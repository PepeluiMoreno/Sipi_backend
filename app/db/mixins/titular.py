class TitularidadMixin:
    """
    Mixin para entidades/organismos que tienen un titular actual 
    y titulares anteriores
    """
    
    # Debe ser definido en cada clase
    DENOMINACION_TITULARIDAD = None  # "obispo", "notario", "registrador", "director"
    
    @property
    def titulares(self):
        """Relación con todos los titulares"""
        return getattr(self, 'titulares')
    
    def _get_titular_actual(self):
        """Obtiene el titular actual (con fecha_fin nulo)"""
        if not hasattr(self, '_titular_actual_cache'):
            titular_actual = next((
                t for t in self.titulares 
                if getattr(t, 'fecha_fin', None) is None
            ), None)
            self._titular_actual_cache = titular_actual
        return self._titular_actual_cache
    
    def _get_titulares_anteriores(self):
        """Lista de titulares anteriores (con fecha_fin no nula)"""
        return [
            t for t in self.titulares 
            if getattr(t, 'fecha_fin', None) is not None
        ]
    
    # Propiedades dinámicas basadas en DENOMINACION_TITULARIDAD
    @property
    def _propiedad_actual(self):
        return f"{self.DENOMINACION_TITULARIDAD}_actual"
    
    @property
    def _propiedad_tiene(self):
        return f"tiene_{self.DENOMINACION_TITULARIDAD}"
    
    @property
    def _propiedad_anteriores(self):
        return f"{self.DENOMINACION_TITULARIDAD}s_anteriores"
    
    def __getattr__(self, name):
        """Genera propiedades dinámicamente basadas en DENOMINACION_TITULARIDAD"""
        if name == self._propiedad_actual:
            return self._get_titular_actual()
        elif name == self._propiedad_tiene:
            return self._get_titular_actual() is not None
        elif name == self._propiedad_anteriores:
            return self._get_titulares_anteriores()
        raise AttributeError(f"'{self.__class__.__name__}' no tiene el atributo '{name}'")