import streamlit as st
import requests
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

# Configuración de la página
st.set_page_config(page_title="Corrector de textos", page_icon="🇪🇸")

# Título de la aplicación
st.title("Corrector de textos")

# Obtener la API key de los secrets de Streamlit
api_key = st.secrets["api_key"]

def keep_alive():
    # Código para mantener la app activa
    print("¡La aplicación sigue activa!")

# Usar BackgroundScheduler en lugar de BlockingScheduler
sched = BackgroundScheduler()
sched.add_job(keep_alive, 'interval', minutes=30)
sched.start()

def corregir_texto(api_key, texto):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": f"sk-tune-{api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama-3.1-405b-instruct",
        "messages": [
            {"role": "system", "content": "Eres un asistente útil que corrige textos en busca de errores ortográficos y gramaticales, y sugiere mejoras de estilo."},
            {"role": "user", "content": f"Por favor, corrige el siguiente texto, identificando errores ortográficos y gramaticales, sugiriendo mejoras de estilo:\n\n{texto}"}
        ],
        "stream": False,
        "frequency_penalty": 0.3,
        "max_tokens": 9000
    }

    try:
        respuesta = requests.post(url, headers=headers, json=payload)
        respuesta.raise_for_status()
        return respuesta.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud: {str(e)}"

def main():
    texto_a_corregir = st.text_area("Ingrese el texto a corregir:", height=200)

    if st.button("Corregir Texto"):
        if texto_a_corregir:
            with st.spinner("Corrigiendo texto..."):
                resultado_correccion = corregir_texto(api_key, texto_a_corregir)
                st.subheader("Resultado de la Corrección:")
                st.write(resultado_correccion)
        else:
            st.error("Por favor, ingrese el texto a corregir.")

if __name__ == "__main__":
    main()
