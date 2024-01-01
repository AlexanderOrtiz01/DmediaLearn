from pynput import keyboard

def on_press(key):
    try:
        print('Tecla presionada: {0}'.format(key.char))
    except AttributeError:
        print('Tecla especial presionada: {0}'.format(key))

def on_release(key):
    print('Tecla liberada: {0}'.format(key))
    if key == keyboard.Key.esc:
        # Si se presiona la tecla "Esc", detener la escucha del teclado
        return False

# Crear un objeto Listener para escuchar los eventos del teclado
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Mantener el programa en ejecución
input('Presiona Enter para detener el programa...')
