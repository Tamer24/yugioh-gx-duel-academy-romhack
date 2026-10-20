@ Gancho al empezar el fin de turno (FUN_0801D7DC, 0x0801D7DC): Stim-Pack pierde 200 de ATK en cada
@ Standby Phase de quien la controla.
@
@ Stim-Pack (ID 4890) no tiene codigo propio: el calculador de ATK (FUN_08012460, caso del equipo)
@ ya le da al monstruo equipado 700 - 200 x contador, con el contador en el byte +0x3A de la
@ ranura del equipo. El motor tiene acciones para ese contador (FUN_0801BAF4 fijar, FUN_0801BB3C
@ sumar 1, FUN_0801BB88 restar 1, FUN_0801BBD4 poner en cero), pero con la carta recortada nadie
@ las pide. Este gancho suma 1 (tope 255) al contador de cada Stim-Pack boca arriba en la zona de
@ Magicas y Trampas del jugador que empieza turno, justo cuando termina el turno del otro: entre
@ ese momento y su Standby Phase solo se roba, asi que el efecto es el mismo. El motor recalcula el
@ ATK en el cambio de fase siguiente.
@
@ El jugador: FUN_0801D7DC toma el de 0x020214E0 (bit 15) como el que termina turno; el que empieza
@ es el otro.
@
@ El gancho pisa las 4 primeras instrucciones de FUN_0801D7DC (que no recibe argumentos),
@     push {r4, r5, r6, r7, lr} ; mov r7, sl ; mov r6, sb ; mov r5, r8
@ las repite al final y sigue en 0x0801D7E4. No llama a nada: lr queda intacto.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7}
    ldr   r0, =0x020214E0
    ldrh  r0, [r0]
    lsrs  r0, r0, #15             @ jugador cuyo turno termina
    movs  r5, #1
    subs  r5, r5, r0              @ r5 = el que empieza turno
    ldr   r6, =0x02022250
    ldr   r0, =0x00002B08
    muls  r0, r5, r0
    adds  r6, r6, r0              @ r6 = cartas de ese lado
    movs  r4, #0
.Lcarta:
    movs  r0, #0x50
    muls  r0, r4, r0
    adds  r7, r6, r0              @ r7 = ranura
    ldrh  r0, [r7, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #16             @ indice * 2
    beq   .Lsiguiente
    ldr   r1, =0x087A8624         @ indice -> ID de Konami
    ldrh  r0, [r0, r1]
    ldr   r1, =4890               @ Stim-Pack
    cmp   r0, r1
    bne   .Lsiguiente
    adds  r1, r7, #0
    adds  r1, #0x30               @ r1 = ranura + 0x30
    ldrb  r0, [r1, #1]
    lsrs  r0, r0, #4              @ zona (+0x31, nibble alto)
    cmp   r0, #5
    bne   .Lsiguiente             @ no esta en la zona de Magicas y Trampas
    ldrb  r0, [r1, #3]
    cmp   r0, #0x20
    beq   .Lsiguiente             @ boca abajo (+0x33): todavia no se activo
    ldrb  r0, [r1, #0xa]          @ contador (+0x3A)
    cmp   r0, #0xff
    beq   .Lsiguiente
    adds  r0, #1
    strb  r0, [r1, #0xa]
.Lsiguiente:
    adds  r4, #1
    cmp   r4, #100
    blt   .Lcarta
    pop   {r4, r5, r6, r7}
    push  {r4, r5, r6, r7, lr}    @ las 4 instrucciones pisadas
    mov   r7, sl
    mov   r6, sb
    mov   r5, r8
    ldr   r3, =0x0801D7E5
    bx    r3
    .align 2
    .pool
