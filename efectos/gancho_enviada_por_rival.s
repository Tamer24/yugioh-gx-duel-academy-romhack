@ Gancho en el procesador de acciones (FUN_08016C36, 0x0801706C): justo despues de que una
@ carta cambia de zona (FUN_080188AC). Pisa las 3 instrucciones
@     adds r0, r6, #0 ; bl FUN_080188AC ; cmp r5, #0xd
@ las repite y sigue en 0x08017072.
@
@ Agrega lo que el motor no trae: "esta carta fue enviada al cementerio por un efecto del
@ rival". El motor marca con el evento 0x3B las destruidas por un efecto (bandera 4) y en
@ batalla (bandera 5), pero nada pone la bandera 6, que es la que lee Fairy Guardian, ni dispara
@ a las cartas recortadas que dependen de eso. Cuando el destino es el cementerio (r5 = 0xD), la
@ accion no es de batalla (bit 0x800 de las banderas de la accion) y la carta causante
@ ([sp+0x54]) la controla el rival del dueno (o, si la accion no trae causante, el efecto que
@ se esta resolviendo en ese momento es del rival):
@   - pone la bandera 6 (evento 0x3B, como hace el motor con la 4 y la 5);
@   - si la carta es Electric Snake (4469) o Minar (4540) y venia de la mano (zona 0xF), o es
@     Penguin Knight (4205) y venia del mazo (zona 0xC), encola su efecto con FUN_080314B4,
@     con los mismos argumentos que usa el motor para Night Assailant (0x080194AC), cuyo
@     disparador "de la mano al cementerio" si existe.
@ Las fn_04 de las tres (robar 2, 1000 de dano, cementerio al mazo) son las originales.
@
@ Butterfly Dagger - Elma (5724) va antes que todo eso: si pasa de la zona de Magicas y Trampas
@ (zona de origen 5) al cementerio, por lo que sea (destruida, o porque el monstruo equipado dejo
@ el campo), se encola su efecto igual que el de Electric Snake; efectos/elma_vuelve.s la devuelve
@ a la mano.
@
@ Dark Necrofear (5222) es la excepcion: la bandera 6 solo se le pone si ademas fue DESTRUIDA
@ (bit 0x40 de las banderas de la accion; medido: 0x9041 con Raigeki del rival, 0x9001 descartada
@ de la mano por Card Destruction del rival). Es lo que lee efectos/gancho_fin_necrofear.s en la
@ End Phase para la posesion: "destroyed ... by your opponent's card effect". El motor solo pone
@ su bandera 4 ("destruida por un efecto") con el bit 0x100 de la accion, que Raigeki y Dark Hole
@ no traen [PROBADO]. Tampoco se le pone si la destruyen mientras esta equipada a un monstruo
@ (zona de origen 5): ahi es una Carta de Equipo y su efecto no vuelve a activarse.
@
@ Entrada: r6 = id de ranura, r1 = destino empaquetado, r5 = zona de destino. Variables del
@ llamador en la pila: [sp+0x50] banderas de la accion, [sp+0x54] ranura causante, [sp+0x5c]
@ zona de origen. Puede usar r0-r3, ip y lr; r4 y r7 se guardan (8 bytes mas de pila).

    .syntax unified
    .thumb
    .text
    .global _start
    .set PILA, 8
_start:
    push  {r4, r7}
    adds  r0, r6, #0
    ldr   r3, =0x080188AD         @ FUN_080188AC(ranura, destino)
    bl    .Lllamar
    cmp   r5, #0xd
    bne   .Lvolver                @ no fue al cementerio
    adds  r0, r6, #0              @ Butterfly Dagger - Elma: de la zona de Magicas al cementerio,
    bl    .Lranura                @ sea quien sea el causante, encola su vuelta a la mano
    adds  r7, r0, #0              @ (efectos/elma_vuelve.s)
    ldrh  r0, [r7, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #16
    ldr   r1, =0x087A8624
    ldrh  r0, [r0, r1]
    ldr   r1, =5724
    cmp   r0, r1
    bne   .Lno_elma
    ldr   r0, [sp, #(0x5c + PILA)]
    cmp   r0, #5
    bne   .Lvolver
    b     .Ldisparar
.Lno_elma:
    ldr   r0, [sp, #(0x50 + PILA)]
    lsls  r0, r0, #20             @ bit 0x800: destruida en batalla
    bmi   .Lvolver
    ldr   r0, [sp, #(0x54 + PILA)]
    cmp   r0, #0xff
    beq   .Lsin_causante
    bl    .Lranura
    ldr   r0, [r0, #0x30]
    lsls  r0, r0, #12
    lsrs  r0, r0, #31             @ quien controla a la causante
    b     .Lcomparar
.Lsin_causante:
    @ Los descartes de la mano y del mazo (FUN_08019598) no anotan causante. Si en este momento
    @ se esta resolviendo un efecto (byte de estado 0x020204C6 distinto de 0; medido: 0x7F con
    @ Delinquent Duo, 0x80 con Needle Worm, 0 fuera de una resolucion), cuenta el lado de la
    @ carta que se resuelve: bit 0 de su cabecera en 0x020204A4 (el motor la borra al terminar).
    ldr   r0, =0x020204C6
    ldrb  r0, [r0]
    cmp   r0, #0
    beq   .Lvolver                @ regla del juego o coste: no es un efecto
    ldr   r0, =0x020204A4
    ldrb  r0, [r0]
    movs  r1, #1
    ands  r0, r1                  @ su lado
.Lcomparar:
    lsrs  r1, r6, #7              @ dueno de la carta enviada
    cmp   r0, r1
    beq   .Lvolver                @ efecto propio
    adds  r0, r6, #0
    bl    .Lranura
    adds  r7, r0, #0              @ r7 = ranura de la carta enviada
    ldrh  r0, [r7, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #16             @ indice * 2
    ldr   r1, =0x087A8624         @ indice -> ID de Konami
    ldrh  r4, [r0, r1]            @ r4 = ID
    ldr   r1, =5222               @ Dark Necrofear
    cmp   r4, r1
    bne   .Lmarcar
    ldr   r0, [sp, #(0x50 + PILA)]
    lsls  r0, r0, #25             @ bit 0x40: destruida
    bpl   .Lvolver                @ Necrofear enviada sin ser destruida (descarte): nada
    ldr   r0, [sp, #(0x5c + PILA)]
    cmp   r0, #5
    beq   .Lvolver                @ destruida estando equipada (zona de Magicas): no se repite
.Lmarcar:
    movs  r0, #0x3b
    adds  r1, r6, #0
    movs  r2, #6
    ldr   r3, =0x08022035         @ evento 0x3B: pone la bandera
    bl    .Lllamar
    adds  r0, r4, #0
    ldr   r4, [sp, #(0x5c + PILA)] @ zona de origen
    ldr   r1, =4469               @ Electric Snake
    cmp   r0, r1
    beq   .Lde_la_mano
    ldr   r1, =4540               @ Minar
    cmp   r0, r1
    beq   .Lde_la_mano
    ldr   r1, =4205               @ Penguin Knight
    cmp   r0, r1
    bne   .Lvolver
    cmp   r4, #0xc                @ del mazo
    bne   .Lvolver
    b     .Ldisparar
.Lde_la_mano:
    cmp   r4, #0xf
    bne   .Lvolver
.Ldisparar:
    ldr   r2, [r7, #0x30]
    lsls  r2, r2, #12
    lsrs  r2, r2, #24             @ zona actual y controlador
    lsls  r2, r2, #8
    orrs  r2, r6
    lsls  r1, r2, #16
    orrs  r1, r2
    lsrs  r0, r6, #7
    lsls  r0, r0, #31
    movs  r2, #0xe4
    lsls  r2, r2, #21
    orrs  r0, r2
    orrs  r0, r6
    ldr   r3, =0x080314B5         @ FUN_080314B4: encola el efecto disparado
    bl    .Lllamar
.Lvolver:
    pop   {r4, r7}
    cmp   r5, #0xd
    ldr   r3, =0x08017073
    bx    r3
.Lllamar:
    bx    r3

@ r0 = id de ranura (bit 7 = lado) -> r0 = direccion de la ranura. Usa r2, r3.
.Lranura:
    lsrs  r2, r0, #7
    movs  r3, #0x7f
    ands  r0, r3
    movs  r3, #0x50
    muls  r0, r3, r0
    ldr   r3, =0x00002B08
    muls  r3, r2, r3
    adds  r0, r0, r3
    ldr   r3, =0x02022250
    adds  r0, r0, r3
    bx    lr
    .align 2
    .pool
