package dao;
import org.eclipse.paho.client.mqttv3.*;
import org.jboss.dmr.JSONParser;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.Throwable;
import java.util.Timer;
import java.util.TimerTask;

/**
 * Clase que implementa MqttCallback para sobreescribir los metodos connectionLost,messageArrived y deliveryComplete.
 */
public class Suscribirse implements MqttCallback
{
	private Notificador noti;
	private int secs;
	
	
	@Override
	public void connectionLost(Throwable cause)
	{

	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws JSONException
	{
		/**
		 * Se inicializa el notificador que envía los mensajes al correo del destinatario	
		 */
		noti = new Notificador();
		System.out.println(". : SE RECIBIÓ ALERTA : .   TOPICO: "+  topic + " MENSAJE: " + message.toString());

		String messageArrived = message.toString();

		try
		{
			if (messageArrived.contains(";;"))
			{
				String[] splittedMsg = messageArrived.split(";;");
				System.out.println(" ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !");
				System.out.println(" !  "+ splittedMsg[0]+ " : Cerradura: " + splittedMsg[1] + "[Activa]"+"!");
				System.out.println(" ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !");
				alertaCerraduraOffline("La cerradura " + splittedMsg[1] + " ha sido desconectada! ");
			}
			else
			{
				JSONObject json = new JSONObject(messageArrived);
				String destinatario = "miguelpuentes1999@gmail.com";
				String mensaje = json.getString("Tipo");
				String asunto = "ALERTA DE SEGURIDAD | YALE";
				noti.sendFromGMail(destinatario, asunto , mensaje);
			}


		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	public void alertaCerraduraOffline(String msg) throws InterruptedException
	{
		Timer timer = new Timer();
		TimerTask tarea = new TimerTask()
		{
			@Override
			public void run()
			{
				noti.sendFromGMail("miguelpuentes1999@gmail.com", "Cerradura Desconectada | YALE", msg);
			}
		};
		timer.schedule(tarea, 31000);
	}
	@Override
	public void deliveryComplete(IMqttDeliveryToken token)
	{

	}

}
