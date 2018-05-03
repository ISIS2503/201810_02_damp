package dao;


import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;

public class Cliente
{

	/**
	 * Atributo que representa el cliente en Mqtt.
	 */
	private MqttClient client;
	
	private Suscribirse suscribirse;
	
	/**
	 * Constante de tipo String que representa la URL del broker.
	 */
	public static final String BROKER_URL = "tcp://172.24.42.81:8083";

	
	/**
	 * MÃ©todo constructor del la clase Cliente que representa un suscriptor Mqtt.
	 */
	public Cliente()
	{
		String clientId = "Administrador";

		try
		{
			client = new MqttClient(BROKER_URL, clientId);
		}
		catch (MqttException e)
		{
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	/**
	 * Metodo en el que se hace la suscripcion a los topicos que define node-red.
	 * @throws InterruptedException 
	 */
	public void start()
	{
		try
		{
			suscribirse = new Suscribirse();
			suscribirse.alertaCerraduraOffline("First");
			client.setCallback(suscribirse);
			client.connect();
			/**
			 * Suscripción al topico de alertas correspondientes a la cerradura: Activo.A1.conjunto.1.1.1 
			 */
			client.subscribe("Activo.A1.conjunto.1.1.1");
			/**
			 * Suscripcion para health check
			 */
			client.subscribe("Activo.A1.conjunto.1.1.1.health-check");
			
		}
		catch (MqttException e)
		{
			e.printStackTrace();
			System.exit(1);
		}
		catch (InterruptedException e)
		{
			e.printStackTrace();
		}
	}
	public static void main(String[] args)
	{
		Cliente client = new Cliente();
		System.out.println("  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ");
		System.out.println("  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - ADMINISTRACIÓN CERRADURAS   -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ");
		System.out.println("  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ");
		client.start();
		while (true)
		{

		}
	}
}