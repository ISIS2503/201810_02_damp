package frame;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;

public class InformacionInmueble extends JPanel
{
	private ModuloControl principal;
	private JLabel nombre;
	private JTextField tnombre;
	private JLabel correo;
	private JTextField tcorreo;
	private JLabel celular;
	private JTextField tcelular;
	private JLabel conjunto;
	private JTextField tconjunto;
	private JLabel torre;
	private JTextField ttorre;
	private JLabel casa;
	private JTextField tcasa;
	private JLabel piso;
	private JTextField tpiso;

	public InformacionInmueble(ModuloControl pModulo)
	{
		//Importanttisisimo NO olvidar.
		principal = pModulo;
		//

		setLayout( new GridLayout(12,2));
		setBorder(new TitledBorder("Informacion Propiedad"));

		nombre = new JLabel("Nombre Propietario: ");
		add(nombre);
		tnombre = new JTextField(" - - - ");
		tnombre.setBackground(Color.white);
		tnombre.setEditable(false);
		add(tnombre);
		
		correo = new JLabel("Correo Propietario: ");
		add(correo);
		tcorreo = new JTextField(" - - - ");
		tcorreo.setBackground(Color.white);
		tcorreo.setEditable(false);
		add(tcorreo);
		
		celular = new JLabel("Numero Celular: ");
		add(celular);
		tcelular = new JTextField(" - - - ");
		tcelular.setBackground(Color.white);
		tcelular.setEditable(false);
		add(tcelular);
		
		conjunto = new JLabel("Nombre Conjunto: ");
		add(conjunto);
		tconjunto = new JTextField(" - - - ");
		tconjunto.setBackground(Color.white);
		tconjunto.setEditable(false);
		add(tconjunto);
		
		torre = new JLabel("Numero Torre: ");
		add(torre);
		ttorre = new JTextField(" - - - ");
		ttorre.setBackground(Color.white);
		ttorre.setEditable(false);
		add(ttorre);
		
		casa = new JLabel("Numero Casa: ");
		add(casa);
		tcasa = new JTextField(" - - - ");
		tcasa.setBackground(Color.white);
		tcasa.setEditable(false);
		add(tcasa);
		
		piso = new JLabel("Numero Piso: ");
		add(piso);
		tpiso = new JTextField(" - - - ");
		tpiso.setBackground(Color.white);
		tpiso.setEditable(false);
		add(tpiso);
		
		JLabel empty = new JLabel("");
		JLabel empty1 = new JLabel("");
		JLabel empty2 = new JLabel("");
		JLabel empty3 = new JLabel("");
		JLabel empty4 = new JLabel("");
		JLabel empty5 = new JLabel("");
		JLabel empty6 = new JLabel("");
		JLabel empty7 = new JLabel("");
		JLabel empty8 = new JLabel("");
		add(empty);
		add(empty1);
		add(empty2);
		add(empty3);
		add(empty4);
		add(empty5);
		add(empty6);
		add(empty7);
		add(empty8);

	}
	public void actualizarInformacion(Propietario p)
	{
		tnombre.setText(p.getNombre());
		tcorreo.setText(p.getCorreo());
		tcelular.setText(p.getCelular());
		tconjunto.setText(p.getConjunto());
		ttorre.setText(p.getTorre());
		tcasa.setText(p.getCasa());
		tpiso.setText(p.getPiso());
		
	}
}
