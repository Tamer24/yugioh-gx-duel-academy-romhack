@ Dark Necrofear (ID 5222), fn_04: la posesion. En el ROM la funcion de su fila es un stub
@ (movs r0, #0 ; bx lr): el efecto no existe y se escribe de cero.
@
@ Texto de la carta: "When this card is destroyed by battle or by your opponent's card effect, in
@ the End Phase of that turn, it is treated as an Equip Spell Card and equipped to 1 of your
@ opponent's monsters. As long as it is equipped to a monster by this effect, you take control of
@ that monster."
@
@ Como llega hasta aca: efectos/gancho_fin_necrofear.s encola el efecto en la End Phase (tipo de
@ efecto 4, momento 5: (cabecera & 0x7FE00) == 0xA800), la fn_18 (efectos/necrofear_seleccion.s)
@ hace elegir un monstruo rival boca arriba y deja la eleccion en p[8] (cantidad, nibble bajo) y
@ p[9] (id de ranura, bit 7 = lado). El motor tambien llamaba a esta funcion apenas Necrofear era
@ destruida en batalla (tipo 4, otro momento): ahi no se hace nada. La receta quita ese disparo
@ (B:0801786E); la guarda queda igual, por si el parche no esta.
@
@ Que hace, con Necrofear todavia en el cementerio y el objetivo en el campo, boca arriba y bajo
@ control del rival:
@   1. busca una zona libre de Magicas y Trampas del que activa (FUN_08011120); sin lugar, nada;
@   2. toma el control del objetivo con FUN_0801A8A4(id, 0), la llamada de Change of Heart; si no
@      se puede (sin zona de monstruo libre), nada;
@   3. pasa a Necrofear del cementerio a esa zona, boca arriba, con FUN_080188AC, como hacen los
@      monstruos Union (0x08061A74): destino = lado << 15 | zona 5 << 10 | casilla << 4 | 8;
@   4. la equipa al objetivo con FUN_0801A600 (evento 0x48: ranura+0x3C de Necrofear = objetivo,
@      y una entrada de tipo 1 en la lista de modificadores del monstruo).
@ Lo demas lo hace el motor: si el monstruo deja el campo, manda sus equipos al cementerio; si la
@ que deja el campo es Necrofear, efectos/gancho_necrofear_equipo.s la hace pasar por Snatch
@ Steal y el procesador de acciones devuelve el monstruo.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0
    ldr   r0, [r4]
    ldr   r1, =0x0007FE00
    ands  r0, r1
    ldr   r1, =0x0000A800         @ tipo de efecto 4, momento 5: el pedido de la End Phase
    cmp   r0, r1
    bne   .Lfin
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldrb  r0, [r4, #8]
    movs  r1, #0xf
    ands  r0, r1
    cmp   r0, #1
    bne   .Lfin                   @ sin eleccion
    ldrb  r5, [r4, #9]            @ r5 = id del objetivo
    ldrb  r7, [r4]
    movs  r0, #1
    ands  r7, r0                  @ r7 = lado que activa
    ldrh  r6, [r4]
    lsls  r6, r6, #23
    lsrs  r6, r6, #24             @ r6 = id de ranura de Necrofear
    adds  r0, r6, #0
    bl    .Lranura
    ldr   r0, [r0, #0x30]
    lsls  r0, r0, #13
    lsrs  r0, r0, #25
    cmp   r0, #0xd
    bne   .Lfin                   @ Necrofear ya no esta en el cementerio
    adds  r0, r5, #0
    bl    .Lranura
    adds  r2, r0, #0              @ r2 = ranura del objetivo
    ldr   r0, [r2, #0x30]
    lsls  r1, r0, #13
    lsrs  r1, r1, #25
    bne   .Lfin                   @ ya no esta en el campo (zona distinta de 0)
    lsls  r0, r0, #12
    lsrs  r0, r0, #31             @ quien lo controla
    cmp   r0, r7
    beq   .Lfin                   @ tiene que controlarlo el rival
    adds  r2, #0x33
    ldrb  r0, [r2]
    lsls  r0, r0, #27
    bpl   .Lfin                   @ boca abajo
    adds  r0, r7, #0
    ldr   r3, =0x08011121         @ FUN_08011120(lado): casilla libre de Magicas y Trampas, o -1
    bl    .Lllamar
    adds  r4, r0, #0              @ r4 = casilla (p ya no hace falta)
    adds  r0, #1
    beq   .Lfin                   @ sin lugar para equiparse
    adds  r0, r5, #0
    movs  r1, #0
    ldr   r3, =0x0801A8A5         @ FUN_0801A8A4(id, 0): pasa el monstruo al otro lado
    bl    .Lllamar
    cmp   r0, #0
    beq   .Lfin                   @ no se pudo tomar el control
    lsls  r1, r7, #15
    lsls  r4, r4, #4
    orrs  r1, r4
    ldr   r0, =0x00001408         @ zona 5 (Magicas y Trampas), boca arriba
    orrs  r1, r0
    adds  r0, r6, #0
    ldr   r3, =0x080188AD         @ FUN_080188AC(id, destino): del cementerio al campo
    bl    .Lllamar
    adds  r0, r7, #0
    adds  r1, r6, #0
    adds  r2, r5, #0
    ldr   r3, =0x0801A601         @ FUN_0801A600(lado, equipo, monstruo): equipa
    bl    .Lllamar
.Lfin:
    movs  r0, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lranura:                         @ r0 = id de ranura -> r0 = direccion (usa r1 y r2)
    movs  r1, #0x7f
    ands  r1, r0
    movs  r2, #0x50
    muls  r1, r2, r1
    lsrs  r0, r0, #7
    ldr   r2, =0x00002B08
    muls  r0, r2, r0
    adds  r0, r0, r1
    ldr   r1, =0x02022250
    adds  r0, r0, r1
    bx    lr
.Lllamar:
    bx    r3
    .align 2
    .pool
