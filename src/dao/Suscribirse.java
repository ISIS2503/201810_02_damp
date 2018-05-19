package dao;
import org.eclipse.paho.client.mqttv3.*;
import org.jboss.dmr.JSONParser;
import org.json.JSONException;
import org.json.JSONObject;

import frame.ModuloControl;

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
	private Notificador noti = new Notificador();
	private Timer timer;
	private TimerTask tarea;
	private ModuloControl modulo;
	
	private boolean A1 = true;
	private boolean A2 = true;
	private boolean A3 = true;
	private boolean A4 = true;
	
	public Suscribirse()
	{
		modulo = new ModuloControl();
		modulo.setVisible(true);
	}
	
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
		
		//noti = new Notificador();
		
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
				String mensajeCompleto = json.getString("Tipo");
				String[] splittedMensaje = mensajeCompleto.split("");
				String mensaje = splittedMensaje[0]+splittedMensaje[1];
				
				String asunto = "ALERTA DE SEGURIDAD | YALE";
				
				if (mensaje.equals("A1") && A1 == true)
				{
//					noti.sendFromGMail(destinatario, asunto , mensaje);
					modulo.pintarAlerta("A1: Puerta Abierta", "red");
				}
				else if (mensaje.equals("A2") && A2 == true)
				{
//					noti.sendFromGMail(destinatario, asunto , mensaje);
					modulo.pintarAlerta("A2: Movimiento Sospechoso", "blue");
				}
				else if (mensaje.equals("A3") && A3 == true)
				{
//					noti.sendFromGMail(destinatario, asunto , mensaje);
					modulo.pintarAlerta("A3: Clave Incorrecta", "orange");
				}
				else if (mensaje.equals("A4") && A4 == true)
				{
//					noti.sendFromGMail(destinatario, asunto , mensaje);
					modulo.pintarAlerta("A4: Bateria Baja", "yellow");
				}
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
				noti.sendFromGMail("miguelpuentes1999@gmail.com", "Cerradura Desconectada | YALE", "Cerradura "+ pMsg +" desconectada");
				modulo.pintarAlerta("ERROR " +" : Cerradura: " + pMsg + "[Inactiva]" ,"gray");
				System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
				System.out.println("!!!!!! ERROR " +" : Cerradura: " + pMsg + "[Inactiva]" + "!!!!!!!!!!!");
				System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
			}
		};
		timer.schedule(tarea, 41000);
	}
	public void desactivarAlarma(String pId)
	{
		if ("A1".equals(pId))
		{
			A1 = false;
		}
		else if ("A2".equals(pId))
		{
			A2 = false;
		}
		else if ("A3".equals(pId))
		{
			A3 = false;
		}
		else if("A4".equals(pId))
		{
			A4 = false;
		}
		
	}
	public void reactivarAlarma(String pId)
	{
		if ("A1".equals(pId))
		{
			A1 = true;
		}
		else if ("A2".equals(pId))
		{
			A2 = true;
		}
		else if ("A3".equals(pId))
		{
			A3 = true;
		}
		else if("A4".equals(pId))
		{
			A4 = true;
		}
	}
	
	
	
	@Override
	public void deliveryComplete(IMqttDeliveryToken token)
	{

	}

}
