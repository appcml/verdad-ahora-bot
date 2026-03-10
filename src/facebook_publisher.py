#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from .utils import log
from .config import FB_PAGE_ID, FB_ACCESS_TOKEN

class FacebookPublisher:
    def __init__(self):
        self.page_id = FB_PAGE_ID
        self.access_token = FB_ACCESS_TOKEN
        self.api_version = "v18.0"
    
    def publicar_contenido(self, contenido, imagen_path):
        """
        Publica contenido viral en Facebook con imagen
        """
        if not self.page_id or not self.access_token:
            log("Faltan credenciales de Facebook", 'error')
            return False
        
        # Preparar mensaje final
        mensaje = f"{contenido['texto_viral']}\n\n{contenido['hashtags']}"
        
        # Truncar si es necesario (límite de Facebook)
        if len(mensaje) > 2000:
            mensaje = mensaje[:1997] + "..."
        
        log(f"Publicando contenido ({len(mensaje)} chars)...", 'facebook')
        
        try:
            if imagen_path and os.path.exists(imagen_path):
                # Publicación con foto (mejor engagement)
                url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/photos"
                
                with open(imagen_path, 'rb') as img_file:
                    files = {'file': img_file}
                    data = {
                        'message': mensaje,
                        'access_token': self.access_token,
                        'published': 'true'
                    }
                    
                    response = requests.post(url, files=files, data=data, timeout=60)
            else:
                # Fallback a publicación de texto con link
                url = f"https://graph.facebook.com/{self.api_version}/{self.page_id}/feed"
                data = {
                    'message': mensaje,
                    'link': contenido['link_original'],
                    'access_token': self.access_token
                }
                response = requests.post(url, data=data, timeout=60)
            
            result = response.json()
            
            if response.status_code == 200:
                post_id = result.get('id') or result.get('post_id')
                log(f"✅ Publicado exitosamente: {post_id}", 'exito')
                return {
                    'success': True,
                    'post_id': post_id,
                    'url': f"https://facebook.com/{post_id}"
                }
            else:
                error_msg = result.get('error', {}).get('message', 'Error desconocido')
                log(f"❌ Error Facebook API: {error_msg}", 'error')
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            log(f"❌ Error en publicación: {e}", 'error')
            return {'success': False, 'error': str(e)}
    
    def programar_publicacion(self, contenido, imagen_path, fecha_hora):
        """
        Programa publicación para fecha específica (requiere permisos adicionales)
        """
        # Nota: La programación requiere permisos especiales de Facebook
        # Por ahora publicamos inmediatamente
        return self.publicar_contenido(contenido, imagen_path)
