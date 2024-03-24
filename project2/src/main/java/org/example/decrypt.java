package org.example;
import net.dv8tion.jda.api.entities.channel.ChannelType;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import javax.crypto.Cipher;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Base64;
import  java.util.List;
public class decrypt extends  ListenerAdapter{
    List<String> idList;
    public decrypt(List<String> idList)
    {
        this.idList = idList;
    }
    //according to string of private key, reform it to original private key
    public static PrivateKey restorePrivateKey(String privateKeyString) throws Exception {
        byte[] privateKeyBytes = Base64.getDecoder().decode(privateKeyString);

        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(privateKeyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA","BC");
        return keyFactory.generatePrivate(keySpec);
    }
    //decrypt ciphertext to plaintext with "RSA" in "ECB" mode
    public static String decrypt(String data, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);

        byte[] dataBytes = Base64.getDecoder().decode(data);
        byte[] decryptedBytes = cipher.doFinal(dataBytes);

        return new String(decryptedBytes);
    }
    @Override
    public void onMessageReceived(MessageReceivedEvent event)
    {
        //make sure message if from humane
        if(event.isFromType(ChannelType.PRIVATE)&&!event.getAuthor().isBot())
        {
            String message = event.getMessage().getContentDisplay();
            if(idList.contains(event.getAuthor().getId()))
            {
                //only decrypt message in certain format:"private key \n\n ciphertext"
                String[] array = message.split("\n\n",2);
                String privateKey = array[0];
                String content = array[1];
                try {
                    PrivateKey p_key  = restorePrivateKey(privateKey);
                    String res = decrypt(content,p_key);
                    //after decrypting, send it back to user
                    event.getAuthor().openPrivateChannel().queue(
                            (channel)->channel.sendMessage(res).queue()
                    );
                }
                catch (Exception e)
                {

                }
            }
            // if a user not in group want to decrypt, refuse
            else
            {
                event.getAuthor().openPrivateChannel().queue((channel) ->
                        channel.sendMessage("You are not in group").queue()
                );
            }

        }
    }

}
