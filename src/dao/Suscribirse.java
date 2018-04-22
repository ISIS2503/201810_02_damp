package dao;
import org.eclipse.paho.client.mqttv3.*;
import org.jboss.dmr.JSONParser;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.Throwable;

/**
 * Clase que implementa MqttCallback para sobreescribir los metodos connectionLost,messageArrived y deliveryComplete.
 */
public class Suscribirse implements MqttCallback
{
	private Notificador noti;
	@Override
	public void connectionLost(Throwable cause)
	{

	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws JSONException
	{
			
		noti = new Notificador();
		
		System.out.println("TOPICO: "+  topic + " MENSAJE: " + message.toString());
		try {
			JSONObject json = new JSONObject(message.toString());
			String destinatario = "miguelpuentes1999@gmail.com";
			String mensaje = json.getString("Tipo");
			String asunto = "ALERTA DE SEGURIDAD | YALE";
			noti.sendFromGMail(destinatario, asunto , mensaje);
		}
		catch (Exception e)
		{
			
		}
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token)
	{

	}

}
