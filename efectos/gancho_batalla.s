@ Gancho en FUN_08067E60 (0x08067E60): la fase de la batalla en que se calcula el dano (la
@ "macro 2" del registro 0x02020C20; ver NOTAS-REVERSE.md, "La batalla y los Neo-Spacian"). Se
@ llama una vez por cuadro y, en su primer cuadro (+0xB = 0), el atacante y el defensor ya estan
@ decididos y nada se calculo todavia: el "inicio del Damage Step" de un efecto.
@
@ Atiende dos cartas nuevas:
@  - Neo-Spacian Glow Moss (6771): si ataca o es atacada, el rival roba 1 carta y la muestra; segun
@    su tipo: Monstruo = termina la Battle Phase; Magica = si Glow Moss ataca, ataque directo (aca:
@    el dano de su ATK al rival y la batalla no se calcula); Trampa = Glow Moss pasa a defensa.
@  - Neo-Spacian Grand Mole (6770): en el Damage Step contra un monstruo, vuelve a la mano con el
@    monstruo contra el que pelea. "Puedes": aca se activa sola cuando Mole seria destruido (el
@    juego no deja escribir una pregunta propia) y solo la controlada por el jugador (lado 0).
@
@ Registro de la batalla (0x02020C20): +0 bit 0 = ataque directo; atacante = (u32 << 11) >> 24;
@ defensor = (u16 en +2 << 19) >> 24; +0xA/+0xB = fase y subfase. Para dar por terminada la batalla
@ sin calcular: +0xA = 6, +0xB = 0 (lo que deja la fase 5 al terminar).
@
@ Reemplaza las 8 bytes de la entrada (push, mov r7,sl, mov r6,sb, mov r5,r8), que repite, y sigue
@ en 0x08067E68. Entrada: r0 = parametro de la funcion (se conserva). El salto del gancho pisa r3.
@ Simbolos del motor: ROBAR, REVELAR, DANIO, CAMBIAR_POSICION, LIMPIAR_ACCIONES, ENVIAR,
@ PROCESAR_ACCIONES.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r0, r4, r5, r6, r7, lr}
    ldr   r4, =0x02020C20         @ r4 = registro de la batalla
    ldrb  r0, [r4, #0xb]
    cmp   r0, #0
    bne   .Lorig                  @ solo el primer cuadro de la fase
    ldr   r0, [r4]
    lsls  r0, r0, #11
    lsrs  r5, r0, #24             @ r5 = ranura del atacante
    ldrb  r0, [r4]
    movs  r1, #1
    tst   r0, r1
    beq   .Lbatalla               @ contra un monstruo
    @ ataque directo: solo Glow Moss (el efecto dice "si ataca"), y la rama de la Magica no hace nada
    adds  r0, r5, #0
    bl    .Lid
    ldr   r1, =6771
    cmp   r0, r1
    bne   .Lorig
    adds  r0, r5, #0
    movs  r1, #2                  @ 2 = ataca, y ya es directo
    bl    .Lmoss
    cmp   r0, #1
    beq   .Lsalir
    b     .Lorig
.Lbatalla:
    ldrh  r0, [r4, #2]
    lsls  r0, r0, #19
    lsrs  r6, r0, #24             @ r6 = ranura del defensor

    @ ---- Glow Moss -------------------------------------------------------------
    adds  r0, r5, #0
    bl    .Lid
    ldr   r1, =6771
    cmp   r0, r1
    bne   .Lmoss_def
    adds  r0, r5, #0              @ ataca Glow Moss
    movs  r1, #1
    bl    .Lmoss
    b     .Lmoss_fin
.Lmoss_def:
    adds  r0, r6, #0
    bl    .Lid
    ldr   r1, =6771
    cmp   r0, r1
    bne   .Lmole
    adds  r0, r6, #0              @ atacan a Glow Moss
    movs  r1, #0
    bl    .Lmoss
.Lmoss_fin:
    cmp   r0, #1
    beq   .Lsalir                 @ la batalla ya termino: no seguir con la fase

    @ ---- Grand Mole ------------------------------------------------------------
.Lmole:
    adds  r0, r5, #0
    bl    .Lid
    ldr   r1, =6770
    cmp   r0, r1
    bne   .Lmole_def
    adds  r0, r5, #0              @ Mole ataca
    adds  r1, r6, #0
    movs  r2, #1
    bl    .Lmole_efecto
    cmp   r0, #1
    beq   .Lsalir
    b     .Lorig
.Lmole_def:
    adds  r0, r6, #0
    bl    .Lid
    ldr   r1, =6770
    cmp   r0, r1
    bne   .Lorig
    adds  r0, r6, #0              @ atacan a Mole
    adds  r1, r5, #0
    movs  r2, #0
    bl    .Lmole_efecto
    cmp   r0, #1
    beq   .Lsalir
    b     .Lorig

.Lorig:                           @ lo que pisa el gancho, y a seguir en el original
    pop   {r0, r4, r5, r6, r7}
    pop   {r3}
    mov   lr, r3
    push  {r4, r5, r6, r7, lr}
    mov   r7, sl
    mov   r6, sb
    mov   r5, r8
    ldr   r3, =0x08067E69         @ 0x08067E68 | 1 (push {r5, r6, r7})
    bx    r3
.Lsalir:                          @ la batalla se dio por terminada: volver sin calcular
    pop   {r0, r4, r5, r6, r7, pc}

@ ---- subrutinas --------------------------------------------------------------------
.Lllamar:
    bx    r3

.Lslot:                           @ r0 = id de ranura -> r0 = direccion de la ranura; usa r1, r2
    movs  r1, #0x7f
    ands  r1, r0
    movs  r2, #0x50
    muls  r1, r2, r1
    lsrs  r0, r0, #7
    ldr   r2, =0x00002B08
    muls  r0, r2, r0
    adds  r0, r0, r1
    ldr   r2, =0x02022250
    adds  r0, r0, r2
    bx    lr

.Lid:                             @ r0 = id de ranura -> r0 = ID de Konami de la carta; usa r1, r2
    push  {lr}
    bl    .Lslot
    ldrh  r0, [r0, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #16             @ indice * 2
    ldr   r1, =0x087A8624         @ indice -> ID de Konami
    ldrh  r0, [r0, r1]
    pop   {r1}
    bx    r1

@ Glow Moss. r0 = ranura de Glow Moss, r1 = 1 si ataca a un monstruo, 2 si ataca directo, 0 si la atacan. Devuelve r0 = 1 si la batalla termino.
.Lmoss:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0              @ r4 = ranura de Glow Moss
    adds  r5, r1, #0              @ r5 = ataca
    lsrs  r6, r4, #7              @ lado de Glow Moss
    movs  r1, #1
    ands  r6, r1
    eors  r6, r1                  @ r6 = lado del rival (el que roba)
    ldr   r0, =0x00002B08
    muls  r0, r6, r0
    ldr   r1, =0x02022250
    adds  r7, r0, r1              @ r7 = datos del rival
    ldr   r1, =0x1c
    ldrh  r0, [r7, r1]
    lsrs  r0, r0, #6
    movs  r1, #0x7f
    ands  r0, r1                  @ cartas en su mazo
    beq   .Lm_nada
    ldr   r1, =0x28a4
    ldrb  r0, [r7, r1]            @ ranura de la proxima carta que roba
    push  {r0}
    bl    .Lslot
    movs  r1, #0x30
    ldrb  r0, [r0, r1]
    movs  r1, #0x1f
    ands  r0, r1                  @ tipo: < 0x15 monstruo, 0x15 Trampa, 0x16 Magica
    adds  r4, r4, #0              @ (r4 sigue siendo Glow Moss)
    mov   ip, r0                  @ ip = tipo de la carta robada
    pop   {r0}
    adds  r1, r0, #0              @ r1 = ranura de la carta
    adds  r0, r6, #0              @ lado del rival
    ldr   r3, =REVELAR
    bl    .Lllamar                @ la muestra
    adds  r0, r6, #0
    movs  r1, #1
    ldr   r3, =ROBAR
    bl    .Lllamar                @ el rival roba 1
    mov   r0, ip
    cmp   r0, #0x15
    blo   .Lm_monstruo
    beq   .Lm_trampa
    @ Magica
    cmp   r5, #1
    bne   .Lm_nada                @ Glow Moss no ataca, o ya ataca directo: no hay que cambiar nada
    adds  r0, r4, #0
    bl    .Lslot
    ldr   r1, [r0, #0x28]         @ ATK de Glow Moss
    adds  r0, r6, #0
    ldr   r3, =DANIO
    bl    .Lllamar                @ ataque directo: el dano de su ATK
    movs  r0, #6                  @ batalla terminada sin calcular
    ldr   r1, =0x02020C20
    strb  r0, [r1, #0xa]
    movs  r0, #0
    strb  r0, [r1, #0xb]
    movs  r0, #1
    b     .Lm_fin
.Lm_monstruo:                     @ termina la Battle Phase (FUN_0801B8E0, el evento 0x64)
    ldr   r3, =0x0801B8E1
    bl    .Lllamar
    movs  r0, #1
    b     .Lm_fin
.Lm_trampa:                       @ Glow Moss a defensa
    lsrs  r0, r4, #7
    movs  r1, #1
    ands  r0, r1                  @ su lado
    adds  r1, r4, #0              @ su ranura
    movs  r2, #0
    movs  r3, #0
    push  {r4}
    ldr   r4, =CAMBIAR_POSICION
    mov   ip, r4
    pop   {r4}
    bl    .Lllamar_ip
    movs  r0, #0
    b     .Lm_fin
.Lm_nada:
    movs  r0, #0
.Lm_fin:
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lllamar_ip:
    mov   r3, ip
    bx    r3

@ Grand Mole. r0 = ranura de Mole, r1 = ranura del otro monstruo, r2 = 1 si Mole ataca.
.Lmole_efecto:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0              @ r4 = ranura de Mole
    adds  r5, r1, #0              @ r5 = ranura del otro
    adds  r6, r2, #0              @ r6 = Mole ataca
    lsrs  r0, r4, #7
    movs  r1, #1
    tst   r0, r1
    bne   .Lme_no                 @ solo la del jugador (lado 0)
    adds  r0, r4, #0
    bl    .Lslot
    adds  r7, r0, #0              @ r7 = direccion de Mole
    adds  r0, r5, #0
    bl    .Lslot                  @ r0 = direccion del otro
    movs  r1, #0x33
    ldrb  r2, [r0, r1]
    movs  r3, #0x20
    tst   r2, r3
    bne   .Lme_no                 @ el otro esta en defensa o boca abajo: Mole no pierde
    ldr   r2, [r0, #0x28]         @ ATK del otro
    ldr   r1, [r7, #0x28]         @ ATK de Mole
    cmp   r6, #0
    bne   .Lme_cmp                @ Mole ataca: pierde si el ATK del otro es igual o mayor
    movs  r0, #0x33
    ldrb  r0, [r7, r0]
    movs  r3, #0x20
    tst   r0, r3
    beq   .Lme_cmp                @ Mole atacada en posicion de ataque: igual
    ldr   r1, [r7, #0x2c]         @ en defensa: pierde si el ATK del otro supera su DEF
    cmp   r2, r1
    bls   .Lme_no
    b     .Lme_si
.Lme_cmp:
    cmp   r2, r1
    blo   .Lme_no
.Lme_si:
    ldr   r3, =LIMPIAR_ACCIONES
    bl    .Lllamar
    adds  r0, r4, #0              @ Mole a la mano
    movs  r1, #4
    adds  r2, r4, #0
    ldr   r3, =ENVIAR
    bl    .Lllamar
    adds  r0, r5, #0              @ el otro a la mano de su dueno
    lsrs  r1, r5, #7
    lsls  r1, r1, #15
    movs  r2, #4
    orrs  r1, r2
    adds  r2, r4, #0
    ldr   r3, =ENVIAR
    bl    .Lllamar
    ldr   r3, =PROCESAR_ACCIONES
    bl    .Lllamar
    movs  r0, #6                  @ batalla terminada sin calcular
    ldr   r1, =0x02020C20
    strb  r0, [r1, #0xa]
    movs  r0, #0
    strb  r0, [r1, #0xb]
    movs  r0, #1
    b     .Lme_fin
.Lme_no:
    movs  r0, #0
.Lme_fin:
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

    .align 2
    .pool
