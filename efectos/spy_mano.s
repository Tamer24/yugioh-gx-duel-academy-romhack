@ The Inexperienced Spy (ID 4848): muestra la mano del rival.
@
@ Reemplaza la columna fn_04 de la carta. En el estado 0x80 hace lo que Ancient
@ Telescope (0x0803E458) pero con la MANO del rival, que es la lista que registra
@ Spiritual Water Art - Aoi (0x0805CFB0). En cualquier otro estado, o si la
@ comprobacion original falla, devuelve 0 (igual que Telescope).
@
@ Entrada: r0 = puntero a la carta (byte *). Salida: estado siguiente (0 = nada).
@ Muestra 1 carta al azar de la mano (el texto dice "select and look at 1").
@ Simbolos: AZAR, ORIGINAL, CLEAR_ZONE, REGISTRAR, DIALOGO (direcciones Thumb, bit 0 en 1).
@
@ Campos del lado (0x02022250 + lado * 0x2B08):
@   mano: lista en +0x2824, cantidad = ((b[+0x1C] & 0x3F) << 1) | (b[+0x1B] >> 7)

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0              @ r4 = carta
    movs  r7, #0                  @ fuera del estado 0x80 devuelve 0, como Telescope: si devolviera
    ldr   r1, =0x0201FD00         @ el 0x80 de ORIGINAL, el motor reabriria la lista al cerrarla
    ldr   r2, =0x000007C6         @ estado de activacion (0x020204C6)
    ldrb  r1, [r1, r2]
    cmp   r1, #0x80
    bne   .Lfin
    ldr   r3, =ORIGINAL           @ comprobacion original: 0x80 o 0 (r0 sigue siendo la carta)
    mov   ip, r3
    bl    .Lllamar
    adds  r7, r0, #0              @ r7 = resultado original
    cmp   r7, #0
    beq   .Lfin

    ldr   r3, =CLEAR_ZONE         @ clear_zone_effects(6, 0)
    mov   ip, r3
    movs  r0, #6
    movs  r1, #0
    bl    .Lllamar

    ldrb  r0, [r4]                @ lado del rival = 1 - (carta[0] & 1)
    movs  r1, #1
    ands  r0, r1
    subs  r0, r1, r0
    ldr   r1, =0x00002B08
    muls  r0, r1, r0
    ldr   r1, =0x02022250
    adds  r5, r0, r1              @ r5 = estructura del rival

    ldrb  r0, [r5, #0x1c]         @ r6 = cartas en su mano
    movs  r1, #0x3f
    ands  r0, r1
    lsls  r0, r0, #1
    ldrb  r1, [r5, #0x1b]
    lsrs  r1, r1, #7
    orrs  r0, r1
    adds  r6, r0, #0
    movs  r7, #0
    cmp   r6, #0
    beq   .Lfin                   @ mano vacia: nada que mirar
    ldr   r3, =AZAR               @ "mira 1 carta": una al azar (la lista del motor muestra los
    mov   ip, r3                  @ nombres de todas las candidatas, asi que elegir a ciegas no
    bl    .Lllamar                @ se puede; el azar es lo que hace Inspection)
    movs  r1, #0xff
    ands  r0, r1
.Lmod:
    cmp   r0, r6
    blt   .Lmodfin
    subs  r0, r0, r6
    b     .Lmod
.Lmodfin:
    ldr   r1, =0x00002824         @ lista de mano
    adds  r1, r1, r5
    ldrb  r0, [r1, r0]
    ldr   r3, =REGISTRAR          @ registra solo esa carta como visible
    mov   ip, r3
    bl    .Lllamar

.Lmostrar:
    ldr   r3, =DIALOGO            @ init_effect_dialogue(0, n, 0x02019F24, 0)
    mov   ip, r3
    movs  r0, #0
    movs  r1, #1
    ldr   r2, =0x02019F24
    movs  r3, #0
    bl    .Lllamar

    ldr   r2, =0x02019F00         @ mismos ajustes que Ancient Telescope
    ldrb  r0, [r2, #0x1f]
    movs  r1, #0x3f
    ands  r0, r1
    strb  r0, [r2, #0x1f]
    ldr   r3, =0x02019F20
    ldrb  r0, [r3]
    movs  r1, #3
    bics  r0, r1
    strb  r0, [r3]
    ldrb  r0, [r2]
    movs  r1, #0xf0
    ands  r0, r1
    movs  r1, #2
    orrs  r0, r1
    strb  r0, [r2]
    movs  r7, #10                 @ estado siguiente

.Lfin:
    adds  r0, r7, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

.Lllamar:                         @ llamada a la direccion en ip (BL no llega al ROM bajo)
    bx    ip

    .pool
