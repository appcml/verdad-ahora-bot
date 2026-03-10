#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime, timedelta

# Añadir el directorio actual al path para poder importar src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importaciones absolutas en lugar de relativas
from src.scraper_referencias import AnalizadorEstilo, GeneradorContenidoViral
from src.imagen_generator import GeneradorImagenesViral
from src.facebook_publisher import FacebookPublisher
from src.utils import log, cargar_json, guardar_json
from src.config import TIEMPO_ENTRE_PUBLICACIONES

class VerdadAhoraBot:
    def __init__(self):
        self.analizador = AnalizadorEstilo()
        self.generador = GeneradorContenidoViral()
        self.imagen_gen = GeneradorImagenesViral()
        self.publisher = FacebookPublisher()
        self.historial_path = 'data/historial.json'
        self.estado_path = 'data/estado.json'
    
    def verificar_tiempo(self):
        """Verifica si ha pasado el tiempo mínimo entre publicaciones"""
        estado = cargar_json(self.estado_path, {'ultima_publicacion': None})
        
        if not estado.get('ultima_publicacion'):
            return True, 0
        
        ultima = datetime.fromisoformat(estado['ultima_publicacion'])
        ahora = datetime.now()
        minutos_transcurridos = (ahora - ultima).total_seconds() / 60
        
        puede = minutos_transcurridos >= TIEMPO_ENTRE_PUBLICACIONES
        faltan = max(0, TIEMPO_ENTRE_PUBLICACIONES - minutos_transcurridos)
        
        return puede, faltan
    
    def ya_publicado(self, titulo):
        """Verifica si ya publicamos algo similar"""
        historial = cargar_json(self.historial_path, {'publicaciones': []})
        titulo_hash = hash(titulo.lower().strip())
        
        for pub in historial['publicaciones'][-50:]:
            if hash(pub.get('titulo', '').lower().strip()) == titulo_hash:
                return True
        return False
    
    def guardar_publicacion(self, contenido, resultado):
        """Guarda registro de la publicación"""
        historial = cargar_json(self.historial_path, {'publicaciones': []})
        
        historial['publicaciones'].append({
            'fecha': datetime.now().isoformat(),
            'titulo': contenido['titulo_original'],
            'estilo': contenido['estilo'],
            'categoria': contenido['categoria'],
            'post_id': resultado.get('post_id'),
            'engagement_esperado': 'alto'
        })
        
        historial['publicaciones'] = historial['publicaciones'][-100:]
        guardar_json(self.historial_path, historial)
        
        estado = {
            'ultima_publicacion': datetime.now().isoformat(),
            'total_publicadas': len(historial['publicaciones']),
            'proxima_publicacion': (datetime.now() + 
                                  timedelta(minutes=TIEMPO_ENTRE_PUBLICACIONES)).isoformat()
        }
        guardar_json(self.estado_path, estado)
    
    def ejecutar(self):
        """Ejecuta el ciclo completo del bot"""
        print("\n" + "="*70)
        print("🤖 VERDAD AHORA - Bot de Contenido Viral")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        puede_publicar, minutos_faltan = self.verificar_tiempo()
        
        if not puede_publicar:
            log(f"⏳ Esperando {minutos_faltan:.0f} minutos para siguiente publicación", 'advertencia')
            return True
        
        log("✅ Iniciando ciclo de publicación", 'exito')
        
        log("🔍 Buscando noticias en fuentes confiables...", 'info')
        noticias = self.analizador.obtener_noticias_frescas()
        
        if not noticias:
            log("❌ No se encontraron noticias", 'error')
            return False
        
        log(f"📰 Encontradas {len(noticias)} noticias potenciales", 'info')
        
        noticia = self.generador.seleccionar_mejor_noticia(noticias)
        
        if self.ya_publicado(noticia['titulo']):
            log("⚠️ Noticia ya publicada anteriormente, buscando alternativa...", 'advertencia')
            noticias.remove(noticia)
            if noticias:
                noticia = self.generador.seleccionar_mejor_noticia(noticias)
            else:
                return False
        
        log(f"🎯 Seleccionada: {noticia['titulo'][:60]}...", 'viral')
        
        log("✨ Transformando en contenido viral...", 'viral')
        contenido = self.generador.crear_variante_viral(noticia)
        
        log(f"🎨 Estilo aplicado: {contenido['estilo']}", 'info')
        log(f"📊 Categoría: {contenido['categoria']}", 'info')
        
        log("🎨 Generando imagen viral...", 'viral')
        imagen_path = self.imagen_gen.crear_imagen_viral(
            contenido['titulo_original'], 
            contenido['estilo']
        )
        
        log("📘 Publicando en Facebook...", 'facebook')
        resultado = self.publisher.publicar_contenido(contenido, imagen_path)
        
        if resultado['success']:
            self.guardar_publicacion(contenido, resultado)
            
            if imagen_path and os.path.exists(imagen_path):
                try:
                    os.remove(imagen_path)
                except:
                    pass
            
            print("\n" + "="*70)
            log("✅ PUBLICACIÓN COMPLETADA", 'exito')
            print(f"📰 {contenido['titulo_original'][:50]}...")
            print(f"🎨 Estilo: {contenido['estilo']}")
            print(f"🔗 Post ID: {resultado.get('post_id')}")
            print(f"⏰ Próxima: {(datetime.now() + timedelta(minutes=60)).strftime('%H:%M')}")
            print("="*70)
            return True
        else:
            log("❌ Falló la publicación", 'error')
            return False

def main():
    bot = VerdadAhoraBot()
    return bot.ejecutar()

if __name__ == "__main__":
    try:
        exit(0 if main() else 1)
    except KeyboardInterrupt:
        log("Bot detenido por usuario", 'advertencia')
        exit(1)
    except Exception as e:
        log(f"Error crítico: {e}", 'error')
        import traceback
        traceback.print_exc()
        exit(1)
