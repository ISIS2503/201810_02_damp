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
	/**
	 * Clase que se encarga de enviar la notificacion al propietario utilizando el servidor de gmail
	 */
	private Notificador noti;
	
	private Timer timer;
	private TimerTask tarea;
	
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
		String messageArrived = message.toString();

		try
		{
			if (messageArrived.contains(";;"))
			{
				JSONObject HealthCheckJson = new JSONObject(messageArrived);
				String value = HealthCheckJson.getString("Valor");
				String[] splittedMsg = value.split(";;");
				System.out.println("-------------------------------------------------------------------------------");
				System.out.println("----" + splittedMsg[0]+ " : Cerradura: " + splittedMsg[1] + "[Activa]" + "----");
				System.out.println("-------------------------------------------------------------------------------");
				timer.cancel();
				alertaCerraduraOffline(splittedMsg[1]);
			}
			else
			{
				System.out.println(" || SE RECIBIÓ ALERTA ||   |TOPICO: "+  topic + " |MENSAJE: " + message.toString());
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

	public void alertaCerraduraOffline(String pMsg) throws InterruptedException
	{
		timer = new Timer();
		tarea = new TimerTask()
		{
			@Override
			public void run()
			{
				noti.sendFromGMail("miguelpuentes1999@gmail.com", "Cerradura Desconectada | YALE", "Cerradura desconectada");
				System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
				System.out.println("!!!!!! ERROR " +" : Cerradura: " + pMsg + "[Inactiva]" + "!!!!");
				System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
			}
		};
		timer.schedule(tarea, 31000);
	}
	@Override
	public void deliveryComplete(IMqttDeliveryToken token)
	{

	}

}
