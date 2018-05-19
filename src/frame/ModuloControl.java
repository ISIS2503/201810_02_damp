package frame;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;

import javax.swing.JFrame;
import javax.swing.JOptionPane;


public class ModuloControl extends JFrame
{
	private Mapa mapa;
	private InformacionInmueble info;
	private PanelAlertas alertas;
	private static Propietario[][] propietarios;
	public ModuloControl()
	{
		propietarios = new Propietario[10][10];
		
		for (int i = 0; i < 10; i++)
		{
			for (int j = 0; j < 10; j++)
			{
				if (i==3 && j == 4)
				{
					propietarios[i][j] = new Propietario(i, j, "Rampart", "rampart@gmail.com", "3136755485", "Kandinsky", 2+"", 2+"" ,2+"");
				}
				else
				{
					propietarios[i][j] = new Propietario(i, j, "Propietario("+i+""+j+")", "Prop"+i+""+j+"@gmail.com", "313"+i+""+i+j+j+""+i+i+j+"", "Kandinsky", i+j+"", i+i+j+"" , i+j+j+"");
				}	
			}
		}
		
		try
		{
//			tablero = new Tablero();
		}
		catch( Exception e )
		{
			JOptionPane.showMessageDialog( this,e.getMessage( ), "Error", JOptionPane.ERROR_MESSAGE );
		}

		setLayout( new BorderLayout( ) );
		setSize(1200,600);
		setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE );
		setLocationRelativeTo( null );
		setTitle( "Modulo de control residencial de cerraduras | YALE |" );
		setVisible(true);
		setResizable(false);

		mapa = new Mapa(this);
		mapa.setPreferredSize(new Dimension(600,600));
		mapa.setBackground(Color.white);
		mapa.setVisible(true);
		add( mapa, BorderLayout.CENTER );
		
		info = new InformacionInmueble(this);
		info.setPreferredSize(new Dimension(300,600));
		info.setBackground(Color.white);
		info.setVisible(true);
		add( info, BorderLayout.EAST );
		
		alertas = new PanelAlertas(this);
		alertas.setPreferredSize(new Dimension(300,600));
		alertas.setBackground(Color.white);
		alertas.setVisible(true);
		add( alertas, BorderLayout.WEST );
		
	}
	
	public Propietario buscarPropietario(int pi, int pj)
	{
		Propietario p = null;
		for (int i = 0; i < 10; i++)
		{
			for (int j = 0; j < 10; j++)
			{
				if (propietarios[i][j].getI() == pi && propietarios[i][j].getJ()==pj)
				{
					p = propietarios[i][j];
				}
			}
		}
		return p;
		
	}
	
	public void actualizarInfo(int pi, int pj)
	{
		info.actualizarInformacion(buscarPropietario(pi, pj));	
	}
	public void pintarAlerta(String pAlerta, String pColor)
	{
		mapa.pintarColor(pColor);
		alertas.agregarAlerta(pAlerta);
	}
	
//	public static void main(String[] args)
//	{
//		ModuloControl a = new ModuloControl();
//		a.pintarAlerta("Alertaaaa dos");
//		a.setVisible(true);
//	}

}
