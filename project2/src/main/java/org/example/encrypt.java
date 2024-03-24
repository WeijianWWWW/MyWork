package org.example;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.entities.channel.ChannelType;
import net.dv8tion.jda.api.entities.channel.concrete.TextChannel;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import javax.crypto.Cipher;
import java.nio.charset.StandardCharsets;
import java.security.PublicKey;
import java.util.Base64;
import  java.util.Map;
import  java.util.List;
import java.security.cert.X509Certificate;

public class encrypt extends ListenerAdapter {
    Map<String, X509Certificate> certMap;
    List<String> idList;
    public encrypt(Map<String,X509Certificate> certMap,List<String> idList)
    {
        this.idList = idList;
        this.certMap = certMap;
    }

    //function to encrypt plaintext
    public static  String encrypt(String text,PublicKey key) throws  Exception
    {
        //indicate encrypt algorithm "RSA", encrypt mode "ECB"
        Cipher encryptCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        encryptCipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] cipherText = encryptCipher.doFinal(text.getBytes(StandardCharsets.UTF_8));
        //return ciphertext in string, use BASE64 to decode it
        return Base64.getEncoder().encodeToString(cipherText);
    }
    @Override
    public void onMessageReceived(MessageReceivedEvent event)
    {
        //indicate receive message only from private channel
        if(event.isFromType(ChannelType.PRIVATE))
        {
            String message = event.getMessage().getContentDisplay();
            User user = event.getAuthor();
            String id = user.getId();
            String name = user.getName();
            if(idList.contains(id))
            {
                X509Certificate cert = certMap.get(id);
                PublicKey publicKey = cert.getPublicKey();
                //send ciphertext to public channel,encrypted with sender public key, no one can decrypt except sender
                try {
                    message = name+": "+message;
                    String res = encrypt(message,publicKey);
                    String channelId = "1216742128500080726";
                    TextChannel channel = event.getJDA().getTextChannelById(channelId);
                    channel.sendMessage(res).queue();
                }
                catch (Exception e)
                {

                }
                //send ciphertext to different group member, encrypted with users' corresponding public key
                for(String user_id:idList)
                {
                    //if target receiver is not sender
                     if(user_id != id)
                     {
                         X509Certificate target_cert = certMap.get(user_id);
                         PublicKey p_key = target_cert.getPublicKey();
                         try {
                             String res = encrypt(message,p_key);
                             JDA jda = event.getJDA();
                             jda.retrieveUserById(id).queue(target -> {
                                 target.openPrivateChannel().queue(privateChannel -> {
                                     privateChannel.sendMessage(res).queue();
                                 });
                             }, failure -> {
                                 System.out.println("Could not retrieve user: " + failure.getMessage());
                             });
                         }
                         catch (Exception e)
                         {

                         }
                     }
                }
            }

        }
    }

}
