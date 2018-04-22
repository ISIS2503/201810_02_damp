package vos;
import org.codehaus.jackson.annotate.*;

public class Notificacion
{

	/**
	 * codigo de la notificacion.
	 */
	private String Activo;
	private String Tipo;
	private String Conjunto;
	private String Torre;
	private String Piso;
	private String Apartamento;

	/**
	 * 
	 */
	public Notificacion(@JsonProperty(value="Activo")String Activo, @JsonProperty(value="Tipo")String Tipo,@JsonProperty(value="Conjunto")String Conjunto,@JsonProperty(value="Torre")String Torre,@JsonProperty(value="Piso")String Piso,@JsonProperty(value="Apartamento")String Apartamento)
	
	{
		this.Activo = Activo;
		this.Tipo = Tipo;
		this.Conjunto = Conjunto;
		this.Torre = Torre;
		this.Piso = Piso;
		this.Apartamento = Apartamento;
	}

	public String getActivo() {
		return Activo;
	}

	public void setActivo(String Activo) {
		this.Activo = Activo;
	}

	public String getTipo() {
		return Tipo;
	}

	public void setTipo(String Tipo) {
		this.Tipo = Tipo;
	}

	public String getConjunto() {
		return Conjunto;
	}

	public void setConjunto(String Conjunto) {
		this.Conjunto = Conjunto;
	}

	public String getTorre() {
		return Torre;
	}

	public void setTorre(String Torre) {
		this.Torre = Torre;
	}

	public String getPiso() {
		return Piso;
	}

	public void setPiso(String Piso) {
		this.Piso = Piso;
	}

	public String getApto() {
		return Apartamento;
	}

	public void setApto(String Apartamento) {
		this.Apartamento = Apartamento;
	}
	
	
}
