@ Gancho al entrar a la Battle Phase (FUN_0801B724, 0x0801B724): Twin Swords of Flashing Light -
@ Tryce (ID 5729) deja atacar dos veces al monstruo equipado.
@
@ FUN_0801B724 corre al entrar a la Battle Phase (la llama FUN_08022124) y le pone la bandera 0xE
@ ("puede volver a atacar") a los monstruos de su arbol de IDs: Hayabusa Knight, Mataza the Zapper,
@ Cyber Twin Dragon y dos mas. Despues de cada ataque, FUN_080666B8 da un ataque mas si el monstruo
@ tiene esa bandera o si uno de sus equipos es Tryce y el equipo la tiene, y la consume (evento
@ 0x3C). El fin de turno (FUN_0801D7DC) la borra. Tryce quedo afuera del arbol al recortarla: aca
@ se le pone la bandera 0xE (FUN_0800E178(id de ranura, 0xE)) a cada Tryce boca arriba en la zona
@ de Magicas y Trampas del jugador de 0x020214E0 (bit 15), el mismo que usa la funcion original.
@
@ El gancho pisa las 4 primeras instrucciones de FUN_0801B724,
@     push {r4, r5, r6, r7, lr} ; mov r7, r8 ; push {r7} ; ldr r0, =0x020214E0
@ las repite al final (con el lr de la entrada) y sigue en 0x0801B72C.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    ldr   r0, =0x020214E0
    ldrh  r0, [r0]
    lsrs  r5, r0, #15             @ r5 = el que empieza turno
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
    ldr   r1, =5729               @ Twin Swords of Flashing Light - Tryce
    cmp   r0, r1
    bne   .Lsiguiente
    adds  r1, r7, #0
    adds  r1, #0x30               @ r1 = ranura + 0x30
    ldrb  r2, [r1, #1]
    lsrs  r2, r2, #4              @ zona (+0x31, nibble alto)
    cmp   r2, #5
    bne   .Lsiguiente             @ no esta en la zona de Magicas y Trampas
    ldrb  r2, [r1, #3]
    cmp   r2, #0x20
    beq   .Lsiguiente             @ boca abajo (+0x33): todavia no se activo
    lsls  r0, r5, #7
    orrs  r0, r4                  @ id de ranura
    movs  r1, #0xe
    ldr   r3, =0x0800E179         @ FUN_0800E178(id de ranura, bandera): la pone
    bl    .Lllamar
.Lsiguiente:
    adds  r4, #1
    cmp   r4, #100
    blt   .Lcarta
    pop   {r4, r5, r6, r7}
    pop   {r3}
    mov   lr, r3
    push  {r4, r5, r6, r7, lr}    @ las 4 instrucciones pisadas
    mov   r7, r8
    push  {r7}
    ldr   r0, =0x020214E0
    ldr   r3, =0x0801B72D
    bx    r3
.Lllamar:
    bx    r3
    .align 2
    .pool
