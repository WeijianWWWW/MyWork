package org.example;
import net.dv8tion.jda.api.JDA;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import java.io.BufferedReader;
import java.io.FileReader;
import java.security.SecureRandom;
import java.security.Security;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import  net.dv8tion.jda.api.JDABuilder;
import  net.dv8tion.jda.api.requests.GatewayIntent;
import org.bouncycastle.asn1.x500.X500Name;
import org.bouncycastle.cert.X509v3CertificateBuilder;
import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;
import org.bouncycastle.operator.ContentSigner;
import org.bouncycastle.operator.jcajce.JcaContentSignerBuilder;
import java.math.BigInteger;
import java.security.*;
import java.security.cert.X509Certificate;
import java.util.Date;
import org.bouncycastle.cert.jcajce.JcaX509v3CertificateBuilder;
import java.util.Map;

 public class KeySystem {
       //set security provider is BouncyCastle
       static
       {
           Security.addProvider(new BouncyCastleProvider());
       }
        public void handle() throws Exception
        {
            //list to store group member id
            List<String> idList  =new CopyOnWriteArrayList<>();
            //hash map store <member id,corresponding certificate>
            Map<String,X509Certificate> certMap =new ConcurrentHashMap<>();

            //initialize the encrypt robot
            JDABuilder builder = JDABuilder.createDefault("MTIxNjc0MjM3MjIzMTA5MDIyNw.Go57c3.AEYBmpna283f1GYW7bnZYEVRhUkGL5lGiHqEI4");
            builder.enableIntents(GatewayIntent.MESSAGE_CONTENT);
            builder.addEventListeners(new encrypt(certMap,idList));
            builder.build();

            //initialize the decrypt robot
            JDABuilder decrypt_bot = JDABuilder.createDefault("MTIxNjgyOTU5MzA2Nzk4Mjg0OA.GFxNRY._iG_pBpCt7Wf0jzWzF9k7iAKQjGJ5_5AcWFqDc");
            decrypt_bot.enableIntents(GatewayIntent.MESSAGE_CONTENT);
            decrypt_bot.addEventListeners(new decrypt(idList));
            decrypt_bot.build();
            //start the thread to update group member id list
            Thread system = new operateMember(idList,certMap);
            system.start();
        }

           //generate a key pair with RSA algorithm
     public  static KeyPair generateKeyPair() throws Exception {
         KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA", "BC");
         generator.initialize(2048, new SecureRandom());
         return generator.generateKeyPair();
     }
          //generate a certificate with certain public key, common name, serial  number
     public  static  X509Certificate generateSelfSignedCertificate(KeyPair keyPair, String dn, BigInteger serial) throws Exception {
         long now = System.currentTimeMillis();
         Date startDate = new Date(now);
         X500Name owner = new X500Name(dn);
         Date endDate = new Date(now + 365 * 24 * 60 * 60 * 1000L);

         X509v3CertificateBuilder builder = new JcaX509v3CertificateBuilder(owner, serial, startDate, endDate, owner, keyPair.getPublic());

         ContentSigner signer = new JcaContentSignerBuilder("SHA256WithRSAEncryption").setProvider("BC").build(keyPair.getPrivate());

         return new JcaX509CertificateConverter().setProvider("BC").getCertificate(builder.build(signer));
     }
            //make sure certificate is unique(serial number)
     public static X509Certificate generateUniqueCertificate(Map<String, X509Certificate> userCerts, String userName,KeyPair pairs) throws Exception {
         KeyPair keyPair = pairs;
         BigInteger serial;
         boolean isUnique;
         do {
             serial = new BigInteger(130, new SecureRandom());
             final BigInteger finalSerial = serial;
             isUnique = userCerts.values().stream()
                     .noneMatch(cert -> cert.getSerialNumber().equals(finalSerial));
         } while (!isUnique);
         return generateSelfSignedCertificate(keyPair, "CN=" + userName, serial);
     }


      //the thread to update group member id list
    class operateMember extends Thread{
        List<String> idList;
        Map<String,X509Certificate> certMap;
        JDABuilder builder;
        public operateMember(List<String> idList,Map<String,X509Certificate> certMap)
        {
            this.certMap = certMap;
            this.idList = idList;
        }
        @Override
        public void run()
        {
            try
            {
                //initialize key management robot
                builder = JDABuilder.createDefault("MTIxOTM5MDgyODMwNTE5MTA5Mg.GLv-Ga.Isz87CHgXW8uojNt8MzmqSUJ_IuwLUxvMZtN6w");
                builder.enableIntents(GatewayIntent.MESSAGE_CONTENT);
                while(true)
                {
                    BufferedReader reader = new BufferedReader(new FileReader("idList.txt"));
                    //each line represents a member id
                    String line = null;
                    List<String> new_list =new CopyOnWriteArrayList<>();
                    while((line=reader.readLine())!=null&&!line.isEmpty())
                    {
                       if(!idList.contains(line)&&!certMap.containsKey(line))   // add a new group member
                       {
                              KeyPair pairs = generateKeyPair();
                              X509Certificate newCert = generateUniqueCertificate(certMap,line,pairs);
                              certMap.put(line,newCert);
                              System.out.println("generate new certificate for "+line+" "+newCert);
                              JDA jda = builder.build();
                              jda.retrieveUserById(line).queue(user -> {
                               user.openPrivateChannel().queue(privateChannel -> {
                                   //distribute private ket to user, the private key is a string encoded with BASE64
                                   String privateKey = Base64.getEncoder().encodeToString(pairs.getPrivate().getEncoded());
                                   privateChannel.sendMessage("Your certificate is created and your private key is:\n "+privateKey).queue();
                               });
                           }, failure -> {
                               System.out.println("Could not retrieve user: " + failure.getMessage());
                           });
                       }
                        new_list.add(line);

                    }
                    //detect if any group member is removed from id list
                    for(String id:idList)
                    {
                        if(!new_list.contains(id))
                        {
                            certMap.remove(id);
                            JDA jda = builder.build();
                            jda.retrieveUserById(id).queue(user -> {
                                user.openPrivateChannel().queue(privateChannel -> {
                                    privateChannel.sendMessage("Your are removed from group ").queue();
                                });
                            }, failure -> {
                                System.out.println("Could not retrieve user: " + failure.getMessage());
                            });
                        }

                    }
                    idList.clear();
                    //update is member id list
                    for(String id:new_list)
                    {
                        idList.add(id);
                    }
                    reader.close();
                    try
                    {
                        Thread.sleep(1500);
                    }
                    catch (Exception e)
                    {

                    }

                }
            }catch (Exception e)
            {
                 e.printStackTrace();
            }

        }
    }
    //start program here
    public static void main(String[] args)
    {
        KeySystem system = new KeySystem();
        try
        {
            system.handle();
        }
        catch (Exception e)
        {

        }

    }
}
