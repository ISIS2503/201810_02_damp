package vos;
import org.codehaus.jackson.annotate.*;

public class Notificacion
{

	/**
	 * codigo de la notificacion.
	 */
	@JsonProperty(value="codigo")
	private String codigo;
	/**
	 * Descripcion Ingrediente.
	 */
	@JsonProperty(value="destinatario")
	private String destinatario;
	
	/**
	 * Traduccion al ingles de la descripcion.
	 */
	@JsonProperty(value="mensaje")
	private String mensaje;
	
	@JsonProperty(value="asunto")
	private String asunto;

	/**
	 * 
	 * @param nombre
	 * @param descripcion
	 * @param idescription
	 */
	public Notificacion(@JsonProperty(value="codigo")String codigo, @JsonProperty(value="destinatario")String destinatario,@JsonProperty(value="mensaje")String mensaje,@JsonProperty(value="asunto")String asunto)
	
	{
		this.codigo = codigo;
		this.destinatario = destinatario;
		this.mensaje = mensaje;
		this.asunto = asunto;
	}

	public String getCodigo() {
		return codigo;
	}

	public void setCodigo(String codigo) {
		this.codigo = codigo;
	}

	public String getDestinatario() {
		return destinatario;
	}

	public void setDestinatario(String destinatario) {
		this.destinatario = destinatario;
	}

	public String getMensaje() {
		return mensaje;
	}

	public void setMensaje(String mensaje) {
		this.mensaje = mensaje;
	}

	public String getAsunto() {
		return asunto;
	}

	public void setAsunto(String asunto) {
		this.asunto = asunto;
	}

}

