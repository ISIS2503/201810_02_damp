package co.edu.clienteExp1;
import org.eclipse.paho.client.mqttv3.*;
import java.lang.Throwable;

/**
 * Clase que implementa MqttCallback para sobreescribir los metodos connectionLost,messageArrived y deliveryComplete.
 */
public class Suscribirse implements MqttCallback
{
     @Override
     public void connectionLost(Throwable cause)
     {
    	 
     }

     @Override
     public void messageArrived(String topic, MqttMessage message)
     {
          System.out.println("TOPICO: "+  topic + " MENSAJE: " + message.toString());
     }

     @Override
     public void deliveryComplete(IMqttDeliveryToken token)
     {
    	 
     }

}
