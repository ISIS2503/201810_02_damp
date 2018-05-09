package dao;


import java.util.Scanner;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;


public class Cliente
{

	/**
	 * Atributo que representa el cliente en Mqtt.
	 */
	private MqttClient client;

	private static Suscribirse suscribirse;

	/**
	 * Constante de tipo String que representa la URL del broker.
	 */
	public static final String BROKER_URL = "tcp://172.24.41.200:8083";


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
			client.subscribe("Activo.A3.conjunto.1.1.1");
			client.subscribe("Activo.A4.conjunto.1.1.1");
			client.subscribe("Activo.A5.conjunto.1.1.1");
			client.subscribe("Activo.A6.conjunto.1.1.1");
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
		client.start();
		Scanner sc = new Scanner(System.in);

		for(;;)
		{
			printMenu();

			int option = Integer.parseInt(sc.nextLine());
			switch(option)
			{
			
			case 1:
				System.out.println("--------- Ingrese el tipo de alarma que desea silenciar (Ej: A1) ---------");
				String pId = sc.nextLine();
				suscribirse.desactivarAlarma(pId);
			break;

			case 2: System.out.println("--------- Ingrese el tipo de alarma que desea reactivar (Ej: A1) ---------");
				String pId1 = sc.nextLine();
				suscribirse.reactivarAlarma(pId1);
			break;
			case 3: System.out.println("--------- Adiós! ---------");
				sc.close();
				return;		  

			default: System.out.println("--------- ¡Opción Inválida!---------");
			}
		}
	}
	private static void printMenu()
	{
		System.out.println("  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ");
		System.out.println("  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  CAPA SPEED  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ");
		System.out.println("  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ");
		System.out.println("1. Silenciar Alarma");
		System.out.println("2. Reactivar Alarma");
		System.out.println("3. Exit");
	}
}