/*******************************************************************************
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package  dao;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class PublicadorClaves {

    /**
     * The main method.
     *
     * @param args the arguments
     * @throws IOException 
     */
    public static void main(String[] args) throws IOException {

        String topic = "Activo.A1.conjunto.1.1.1.config";
        int index = 0;
        String newPassword = "";
        String key = "";
        String content = "";
        
        //Formato
        //ADD_PASSWORD;<index>;<newPassword>
        //UPDATE_PASSWORD;<index>;<newPassword>
        //DELETE_PASSWORD;<index>
        //DELETE_ALL
        //COMPARE_KEY;<key>
        
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in)); 
        System.out.println("Por favor elija la acción que quiere llevar a cabo:");
        System.out.println("1 para agregar contraseña, 2 para modificar contraseña, 3 para eliminar contraseña, 4 para eliminar todo, 5 para compare key");
        String accion = br.readLine();
        
        if(accion.equals("1")) {
        	BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        	System.out.println("Escriba el índice de clave a agregar");    
        	String indice = in.readLine();
        	index = Integer.parseInt(indice);
        	BufferedReader clave = new BufferedReader(new InputStreamReader(System.in));
        	System.out.println("Escriba nueva clave de 4 dígitos:");
        	newPassword = clave.readLine();
        	content = "ADD_PASSWORD;" + index + ";" + newPassword;
        }
        else if(accion.equals("2")) {
        	BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        	System.out.println("Escriba el índice de clave a modificar");    
        	String indice = in.readLine();
        	index = Integer.parseInt(indice);
        	BufferedReader clave = new BufferedReader(new InputStreamReader(System.in));
        	System.out.println("Escriba nueva clave de 4 dígitos:");
        	newPassword = clave.readLine();
        	content = "UPDATE_PASSWORD;" + index + ";" + newPassword;
        }
        else if(accion.equals("3")) {
        	BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        	System.out.println("Escriba el índice de clave a eliminar");    
        	String indice = in.readLine();
        	index = Integer.parseInt(indice);        	
        	content = "DELETE_PASSWORD;" + index;
        }
        else if(accion.equals("4")) {
        	System.out.println("Se elimina todo");        	
        	content = "DELETE_ALL";
        }
        else if(accion.equals("5")) {
        	BufferedReader llave = new BufferedReader(new InputStreamReader(System.in));
        	System.out.println("Escriba el índice de clave a eliminar");    
        	key = llave.readLine();       	
        	content = "COMPARE_KEY;" + key;
        }
          
        /**
        String content = "//ADD_PASSWORD;" + index + ";<newPassword>" + 
        		"\n" + 
        		"//UPDATE_PASSWORD;"+ index + ";<newPassword>" + 
        		"\n" + 
        		"//DELETE_PASSWORD;" + index  + 
        		"\n" + 
        		"//DELETE_ALL" + 
        		"//COMPARE_KEY;" + key;     		
        **/
        
        int qos = 2;
        String broker = "tcp://172.24.41.200:8083";
        String clientId = "JavaSample";
        MemoryPersistence persistence = new MemoryPersistence();

        try {
            
            MqttClient sampleClient = new MqttClient(broker, clientId, persistence);
            MqttConnectOptions connOpts = new MqttConnectOptions();
            connOpts.setCleanSession(true);
            System.out.println("Connecting to broker: " + broker);
            sampleClient.connect(connOpts);
            System.out.println("Connected");
            System.out.println("Publishing message: " + content);
            MqttMessage message = new MqttMessage(content.getBytes());
            message.setQos(qos);
            sampleClient.publish(topic, message);
            System.out.println("Message published");
            sampleClient.disconnect();
            System.out.println("Disconnected");
                        
        } catch (MqttException me) {
            System.out.println("reason " + me.getReasonCode());
            System.out.println("msg " + me.getMessage());
            System.out.println("loc " + me.getLocalizedMessage());
            System.out.println("cause " + me.getCause());
            System.out.println("excep " + me);
            me.printStackTrace();
            
        }
    }
}