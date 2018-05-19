package frame;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;

/**
 * @author Miguel Puentes
 *
 */



public class Mapa extends JPanel implements ActionListener

{


	/**
	 * Matrices.
	 */

	private JButton[][] botonesCasillas;
	private ModuloControl principal;


	public Mapa(ModuloControl pPrincipal)
	{
		principal = pPrincipal;
		setBorder(new TitledBorder("Mapa Residencial"));
		setLayout( new GridLayout( 10, 10) );
		botonesCasillas = new JButton[10][10];
		ImageIcon house = new ImageIcon("./data/Images/house.png");
		
		for( int i = 0; i < 10; i++ )
		{
			for( int j = 0; j < 10; j++ )
			{
				botonesCasillas[ i ][ j ] = new JButton( );
				botonesCasillas[ i ][ j ].addActionListener( this );
				botonesCasillas[ i ][ j ].setBackground(Color.WHITE);
				botonesCasillas[ i ][ j ].setIcon(house);
				botonesCasillas[ i ][ j ].setActionCommand( i + ";" + j );
				add( botonesCasillas[ i ][ j ] );
			}
		}
		
	}

//	public void actualizar(){
//		for (int i = 0; i < 5; i++) {
//			for (int j = 0; j< 5; j++) 
//			{
//				if(principal.darCasillas()[i+2][j+2].darEstado() == true)
//				{
//					ImageIcon relleno = new ImageIcon("data/imagenes/casilla_rellena.png");
//					botonesCasillas[ i+2 ][ j+2 ].setIcon(relleno);
//					botonesCasillas[ i+2 ][ j+2 ].setBackground(Color.BLACK);
//					//Colores.
//				}else {
//					ImageIcon sinRelleno = new ImageIcon("data/imagenes/casilla_blanco.jpg");
//					botonesCasillas[ i+2 ][ j+2 ].setIcon(sinRelleno);
//					botonesCasillas[ i+2 ][ j+2 ].setBackground(Color.WHITE);
//				}
//
//			}
//		}
//	}
//
//	public void iniciar(){
//		for (int i = 0; i < 7; i++)
//		{
//			for (int j = 0; j < 7; j++)
//			{
//
//				if(i>1 && j>1){
//					botonesCasillas[i][j].setText("");
//					botonesCasillas[i][j].setEnabled(true);
//					//COLORES
//				}else{
//
//					botonesCasillas[i][j].setText(principal.darCasillas()[i][j].darContenido());
//				}
//
//			}
//		}
//	}

	public void pintarColor(String pColor)
	{
		if (pColor.equals("red"))
		{
			botonesCasillas[ 3 ][ 4 ].setBackground(Color.red);
		}
		else if(pColor.equals("orange"))
		{
			botonesCasillas[ 3 ][ 4 ].setBackground(Color.orange);
		}
		else if(pColor.equals("blue"))
		{
			botonesCasillas[ 3 ][ 4 ].setBackground(Color.blue);
		}
		else if(pColor.equals("yellow"))
		{
			botonesCasillas[ 3 ][ 4 ].setBackground(Color.yellow);
		}
		else if(pColor.equals("gray"))
		{
			botonesCasillas[ 3 ][ 4 ].setBackground(Color.gray);
		}
	}
	public void actionPerformed (ActionEvent evento)
	{
		String comando = evento.getActionCommand( );
		String[] coordenada = comando.split( ";" );
		int i = Integer.parseInt( coordenada[ 0 ] );
		int j = Integer.parseInt( coordenada[ 1 ] );
		principal.actualizarInfo(i, j);
	}
}
