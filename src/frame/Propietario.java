package frame;

public class Propietario
{
	private int i;
	private int j;
	private String nombre;
	private String correo;
	private String celular;
	private String conjunto;
	private String torre;
	private String casa;
	private String piso;


	public Propietario(int pi, int pj, String pNombre,String pCorreo, String pCelular, String pConjunto, String pTorre, String pCasa, String pPiso)
	{
		i = pi;
		j = pj;
		nombre = pNombre;
		correo = pCorreo;
		celular = pCelular;
		conjunto = pConjunto;
		torre = pTorre;
		casa = pCasa;
		piso = pPiso;
	}


	public int getI() {
		return i;
	}


	public void setI(int i) {
		this.i = i;
	}


	public int getJ() {
		return j;
	}


	public void setJ(int j) {
		this.j = j;
	}


	public String getNombre() {
		return nombre;
	}


	public void setNombre(String nombre) {
		this.nombre = nombre;
	}


	public String getCorreo() {
		return correo;
	}


	public void setCorreo(String correo) {
		this.correo = correo;
	}


	public String getCelular() {
		return celular;
	}


	public void setCelular(String celular) {
		this.celular = celular;
	}


	public String getConjunto() {
		return conjunto;
	}


	public void setConjunto(String conjunto) {
		this.conjunto = conjunto;
	}


	public String getTorre() {
		return torre;
	}


	public void setTorre(String torre) {
		this.torre = torre;
	}


	public String getCasa() {
		return casa;
	}


	public void setCasa(String casa) {
		this.casa = casa;
	}


	public String getPiso() {
		return piso;
	}


	public void setPiso(String piso) {
		this.piso = piso;
	}


}
