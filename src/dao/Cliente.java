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
	public static final String BROKER_URL = "tcp://172.24.41.200:8083";

	
	/**
	 * Método constructor del la clase Cliente que representa un suscriptor Mqtt.
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
	 */
	public void start()
	{
		try
		{
			suscribirse = new Suscribirse();
			client.setCallback(suscribirse);
			client.connect();
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
	}
	public static void main(String[] args)
	{
		Cliente client = new Cliente();
		System.out.println(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
		System.out.println(" - - - - - - - - Topicos - - - - - - - - - - - - - - - - - - Mensajes  - - - - - - ");
		System.out.println(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
		client.start();
		while (true)
		{

		}
	}
}