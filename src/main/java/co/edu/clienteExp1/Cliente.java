package co.edu.clienteExp1;


import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;

public class Cliente
{

	/**
	 * Atributo que representa el cliente en Mqtt.
	 */
	private MqttClient client;
	
	/**
	 * Constante de tipo String que representa la URL del broker.
	 */
	public static final String BROKER_URL = "tcp://172.24.42.76:8083";

	
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
	 * Método en el que se hace la suscripcion a los topicos que define node-red.
	 */
	public void start()
	{
		try {
			client.setCallback(new Suscribirse());
			client.connect();
			client.subscribe("Activo/A1/conjunto/1/1/1");
			client.subscribe("Activo/A2/conjunto/1/1/1");
			client.subscribe("Activo/A3/conjunto/1/1/1");
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
		client.start();
		System.out.println(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
		System.out.println(" - - - - - - - - Topicos - - - - - - - Mensajes  - - - - - - ");
		System.out.println(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
		while (true)
		{

		}
	}
}