package frame;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;

import javax.swing.DefaultListModel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.border.TitledBorder;

public class PanelAlertas extends JPanel
{

	private JList<String> listaAlertas;
	private DefaultListModel<String> l1;
	private ModuloControl principal;

	public PanelAlertas(ModuloControl pPrincipal)
	{
		principal = pPrincipal;
		setLayout( new FlowLayout());
		setBorder(new TitledBorder("Alertas en el conjunto"));

		l1 = new DefaultListModel<>();  
		l1.addElement("Example1");  
		listaAlertas = new JList<>(l1);  
		//      listaAlertas.setBounds(100,100, 75,75);  
		add(listaAlertas);  


	}
	public void agregarAlerta(String pAlerta)
	{
		l1.addElement(pAlerta);
		
	}


}
