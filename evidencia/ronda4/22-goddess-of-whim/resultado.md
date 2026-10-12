carta: Goddess of Whim (fila 22)
resultado: COINCIDE
esperado: Avisa si acertaste y el ATK pasa de 950 a 1900 o a 475 hasta el fin del turno.
visto: Se invocó Goddess of Whim (ATK 950, DEF 700), se abrió Activate Effect y apareció "Select heads or tails." Seis tiradas desde el mismo punto (paso 3). En todas el cartel de la moneda, el aviso y el ATK final coinciden:
  T1 Heads, sin espera: cartel "Correct!" -> aviso "You called it right! ATK doubled." -> ATK 1900.
  T2 Heads, w7 antes: cartel "Miss!" -> aviso "You called it wrong... ATK halved." -> ATK 475.
  T3 Heads, w19 antes: cartel "Correct!" -> aviso "You called it right! ATK doubled." -> ATK 1900.
  T4 Tails (DOWN, A), sin espera: cartel "Miss!" -> aviso "You called it wrong... ATK halved." -> ATK 475.
  T5 Tails, w7 antes: cartel "Correct!" -> aviso "You called it right! ATK doubled." -> ATK 1900.
  T6 Tails, w33 antes: cartel "Miss!" -> aviso "You called it wrong... ATK halved." -> ATK 475.
  Aciertos: T1, T3, T5 (1900). Errores: T2, T4, T6 (475). Ningún caso mezclado.
  Nota: la primera tirada de T2 (con capturas espaciadas) no mostró el cartel; se repitió con capturas cada 10 cuadros, mismas teclas, y ahí se vio "Miss!". La repetición quedó en la cadena (pasos 6 y 7); el resultado usado es el de la repetición densa. Mirada en la captura; el ATK 950 de la barra inferior se queda así durante el aviso y cambia recién al cerrarlo, por eso el ATK final se lee de la salida tras el A.
antes: 003.png — "Select heads or tails." (monstruo ATK 950, DEF 700, zona 2)
despues: 016.png — "Goddess of Whim (ataque, ATK 475, DEF 700)" (T6; el caso 1900 es 005.png, 010.png, 014.png)
capturas clave:
  003.png — prompt "Select heads or tails." con Heads marcado
  004-a.png — cartel "Correct!" con la moneda (T1)
  004-d.png — aviso "You called it right! ATK doubled." (T1)
  007-h.png — cartel "Miss!" (T2, repetición densa)
  007-p.png — aviso "You called it wrong... ATK halved." (T2)
  014.png — salida con ATK 1900 tras cerrar el aviso (T5)
diferencias con la guía: la guía dice que el ATK queda así "hasta el fin del turno"; esto no se comprobó (solo se leyó el ATK inmediatamente después de cerrar el aviso, sin pasar de turno). Ningún otro paso se desvió.
pasos usados: 16 (el paso 0 es el de inicio); 6 tiradas + 1 repetición de T2 + invocación y activación
verificado: 6 de 6 tiradas coherentes; además 12 corridas por script: el resultado de la moneda del juego y el ATK coinciden siempre.
