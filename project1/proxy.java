import java.net.*;
import java.io.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;


public class proxy {
     
    public static void main(String[] args) throws IOException
    {
        /*initialize port 8080 to receive from local computer port */
        int local_port = 8080;
        List<String> blockList = new CopyOnWriteArrayList<String>();
        Thread blockHelper = new BlockHelper(blockList);
        blockHelper.start();
        ConcurrentHashMap<String,byte[]> cacheMap = new ConcurrentHashMap<>();
        ServerSocket proxy_socket = new ServerSocket(local_port);
        System.out.println("Proxy socket opens, waiting for contact");
        for(;;)
        {
            /*if new port try to establish connection, a new socket created, othersiwe it got stuck */
            Socket socket  = proxy_socket.accept();
            Thread t = new Handler(socket,cacheMap,blockList);
            t.start();
        }

    }
}
/*the thread help  manage block specific URL */
class BlockHelper extends Thread{
    List<String> blockList;
    public BlockHelper(List<String> blockList)
    {
     this.blockList = blockList;
    }

    @Override 
    public void run()
    {
        try{
            /*continuously read bolck text, update blocked URL list */
            while(true)
            {
                BufferedReader reader = new BufferedReader(new FileReader("Block.txt"));
                blockList.clear();
                String line;
                while((line = reader.readLine())!=null&&!line.isEmpty())
               {
                    blockList.add(line);
                }
                reader.close();
                try
            {
                Thread.sleep(1500);
            }
            catch(InterruptedException e)
            { 
              
            }
            }
        }
        catch(IOException e)
        {
            e.printStackTrace();
        }
       
    }
}

/*the thread generally handle http&https request, estiablish alive connection */
class Handler extends Thread{
    Socket socket;Map<String,byte[]> cacheMap;
    List<String> blockList;
    public Handler(Socket socket,Map<String,byte[]> cacheMap,List<String> blocList)
    {
        this.blockList = blocList;
        this.socket = socket;
        this.cacheMap = cacheMap;
    }


    @Override
    public void run()
    {
        try{
           BufferedReader clientReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
           BufferedWriter clientWriter  = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
           String requestLine  = clientReader.readLine();
           if(requestLine!=null)
           {
               String method = requestLine.split(" ")[0];
            /* handle https request, detect if request line starting with "Connect" */
           if(method.equalsIgnoreCase("Connect"))
           {
                String  requestHeader;String host="";
                while((requestHeader = clientReader.readLine())!=null&&!requestHeader.isEmpty())
                {
                      String[] header_array = requestHeader.split(": ");
                      if(header_array[0].equalsIgnoreCase("Host"))
                      {
                         host = header_array[1];
                      }
                }
                String[] host_array = host.split(":");
                String host_name = host_array[0];
                Boolean contains  = false;
                System.out.println(requestLine);
                /*detect if https request is blocked,also need to read https header */
                for(int i=0;i<blockList.size();i++)
                {
                    if(blockList.get(i).contains(host_name))
                    {
                        contains =true;
                        System.out.println(blockList.get(i)+ " is blocked");
                    }
                }
                if(!contains)
                {
                    if(host_array.length>1)
                {
                  String hostName = host_array[0];
                  int port = Integer.parseInt(host_array[1]);
                  Socket webSocket  = new Socket(hostName,port);
                  /*tell client connection is established successfully */
                  clientWriter.write("HTTP/1.1 200 Connection Established\r\n\r\n");
                  clientWriter.flush();
                  Thread fromClient = new forwardHandler(socket,webSocket);
                  fromClient.start();
                  Thread fromServer = new forwardHandler(webSocket, socket);
                  fromServer.start();
                }
                }
            }

            /*handle http request here */
           else
           {
            String requestHeader;String host ="";
            String url = requestLine.split(" ")[1];
            StringBuilder builder = new StringBuilder();
            builder.append(requestLine+"\r\n");
            while((requestHeader = clientReader.readLine())!=null&&!requestHeader.isEmpty())
            {
                  String[] header_array = requestHeader.split(": ");
                  if(header_array[0].equalsIgnoreCase("Host"))
                  {
                     host = header_array[1];
                  }
                  builder.append(requestHeader+"\r\n");
            }
            builder.append("\r\n");
            System.out.println(builder.toString());
            /*detect if URL is blocked */
            boolean contains = false;
            for(int i=0;i<blockList.size();i++)
            {
                if(blockList.get(i).contains(url))
                {
                    contains = true;
                    System.out.println(blockList.get(i)+" is blocked");
                }
            }
            if(!contains)
            {
                /*detect if URL is cached */
                if(cacheMap.containsKey(url))
                {
                  System.out.println("already cached");
                  byte[] res =cacheMap.get(url);
                  socket.getOutputStream().write(res);
                  socket.getOutputStream().flush();
                }
                else 
                {
                /* if URL is not cached then save it */ 
                String[] host_array = host.split(":");
                String hostName = host_array[0];
                int port = host_array.length>1? Integer.parseInt(host_array[1]):80;
                Socket webSocket  = new Socket(hostName,port);
                BufferedWriter webWriter = new BufferedWriter(new OutputStreamWriter(webSocket.getOutputStream()));
                webWriter.write(builder.toString());
                webWriter.flush();  
                /*finish read from inputStream and transfer to server then receive it  */
                byte[] buffer  = new byte[1024];
                ByteArrayOutputStream buffers = new ByteArrayOutputStream();
                int byteRead;webSocket.setSoTimeout(1000);
                try
                {
                    while((byteRead = webSocket.getInputStream().read(buffer))!=-1)
                  {
                     buffers.write(buffer,0,byteRead);
                  }
                }
                catch(SocketTimeoutException e)
                {
                    buffers.flush();
                    byte[] array = buffers.toByteArray();
                    socket.getOutputStream().write(array);
                    socket.getOutputStream().flush();
                    /*save URL and its corresponding byte array */
                    cacheMap.put(url,array);
                }
                Thread thread1 = new fromServer(socket, webSocket,cacheMap,blockList);
                thread1.start();
                }
            }
           }
           }
    }
    catch(Exception e)
    {
        
    }

}
}
/*the thread handle http request, reading content from stream and cache it,establish link between URL and its content */
class  fromServer extends Thread
{
    Socket inSocket;
    Socket outSocket;
    Map<String,byte[]> cacheMap;
    List<String> blockList;
    public fromServer(Socket inSocket,Socket outSocket, Map<String,byte[]> cacheMap,List<String> blockList)
    {
        this.blockList = blockList;
        this.inSocket = inSocket;
        this.outSocket = outSocket;
        this.cacheMap = cacheMap;
    }
    @Override
     public void run()
     {
        try
        {
            BufferedReader reader = new BufferedReader(new InputStreamReader(inSocket.getInputStream()));
            while(true)
            {
                String requestLine;
                requestLine = reader.readLine();
                if(requestLine!=null)
                {
                  StringBuilder builder = new StringBuilder();
                  builder.append(requestLine+"\r\n");
                  String url  =requestLine.split(" ")[1];
                  String requestHeader;
                  while(!(requestHeader = reader.readLine()).isEmpty())
                  {
                    builder.append(requestHeader+"\r\n");
                  }
                  builder.append("\r\n");
                  System.out.println(builder.toString());
                  
                  /*detect if URL is blocked */
                  boolean contains = false;
                  for(int i=0;i<blockList.size();i++)
                  {
                    if(blockList.get(i).contains(url))
                    {
                        contains = true;
                        System.out.println(blockList.get(i)+ " is blocked");
                    }
                  }
                  if(!contains)
                  {

                  /*detect if URL is cached */
                    if(cacheMap.containsKey(url))
                    {
                      System.out.println("The request is already cached");
                       byte[] res = cacheMap.get(url);
                       inSocket.getOutputStream().write(res);
                       inSocket.getOutputStream().flush();
                    }
                    else
                  /*if URL is not cached, then read it and cache its byte array */
                    {
                    outSocket.getOutputStream().write(builder.toString().getBytes());
                    outSocket.getOutputStream().flush();
                    byte[] buffer  = new byte[2048];
                    ByteArrayOutputStream buffers = new ByteArrayOutputStream();
                    int byteRead;
                    outSocket.setSoTimeout(1000);
                    try
                    {
                      while((byteRead = outSocket.getInputStream().read(buffer))!=1)
                      {
                           buffers.write(buffer, 0, byteRead);
                      }
                    }
                    catch(SocketTimeoutException e)
                    {
                      buffers.flush();
                    }
                    byte[] res = buffers.toByteArray();
                    cacheMap.put(url,res);
                    inSocket.getOutputStream().write(res);
                    }
                    
                  }
                  
                }
            }
        }
        catch(Exception e)
        {
     
        } 
     }
   

}
/*the thread simply transfer data from server, without reading content,so it is  for https request */
class forwardHandler extends Thread{
    Socket inSocket;
    Socket outSocket;
    public forwardHandler(Socket inSocket, Socket outSocket)
    {
        this.inSocket = inSocket;
        this.outSocket = outSocket;
    }

    @Override
    public void run()
    {
        try{
            
                InputStream input =  inSocket.getInputStream();
                OutputStream output = outSocket.getOutputStream();
                output.flush();
                int byteRead;
                byte[] buffer = new byte[1024];
                /*forward data while reading it,  */
                while((byteRead = input.read(buffer))!=-1)
                {
                    output.write(buffer,0,byteRead);
                    output.flush();
                }
                try{
                    Thread.sleep(10);
                }catch(InterruptedException e)
                {
                  
                }
            
        }
        catch(IOException e)
        {
            
        }    
    }
}



