# Duel Academy Hack v0.1

Fecha: 2026-10-11. 6 cartas restauradas, todas probadas en duelo y confirmadas a ojo.

## Cómo se usa

1. Hace falta el ROM original *Yu-Gi-Oh! GX - Duel Academy (USA)*, MD5 `f62c47cbe08e1e3bcfcf9f1b84841a76`.
2. Aplicar el parche: `python3 scripts/bps.py --aplicar "ROM original.gba" build/hack-v0.1.bps "Yu-Gi-Oh! GX - Duel Academy (Hack v0.1).gba"` (o cualquier programa que aplique `.bps`).
3. El ROM que sale tiene MD5 `668e43e7a8b85391c0f1e15d11212b05`. El parche tiene MD5 `bb32d35a35f85fe08c97d217b08d65c7`.

Las cartas nuevas ocupan el lugar de monstruos Normales y aparecen en los sobres donde salían ellos; también se pueden comprar con su contraseña. Todavía muestran el dibujo del monstruo que reemplazan.

## Cartas

| Carta | N.º | Reemplaza a | Clase | Contraseña |
|---|---|---|---|---|
| Dark-Eyes Illusionist | 57 | Fiend's Hand | Spellcaster / Effect | 38247752 |
| Jowls of Dark Demise | 520 | Souleater | Fiend / Effect | 05257687 |
| Magic Drain | 536 | Grand Tiki Elder | Trap Counter | 59344077 |
| Reaper of the Cards | 971 | Pharaoh's Servant | Fiend / Effect | 33066139 |
| Rigorous Reaver | 524 | Boneheimer | Plant / Effect | 39180960 |
| Windstorm of Etaqua | 489 | Flying Kamakiri #2 | Trap | 59744639 |

## Qué quedó afuera

Cartas del lote que no entran en esta versión y qué les falta:

- Acid Trap Hole: confirmacion a ojo
- Big Burn: confirmacion a ojo
- Chosen One: confirmacion a ojo
- Dark Necrofear: veredicto funciona en parte, confirmacion a ojo, prueba de logica (Unicorn)
- Electric Snake: confirmacion a ojo
- Electromagnetic Bagworm: veredicto funciona en parte, confirmacion a ojo
- Exchange: confirmacion a ojo
- Fairy Guardian: confirmacion a ojo
- Goddess of Whim: confirmacion a ojo
- Hiro's Shadow Scout: confirmacion a ojo
- Kunai with Chain: confirmacion a ojo
- Lady Panther: confirmacion a ojo
- Minar: confirmacion a ojo
- Monster Recovery: confirmacion a ojo
- Mystical Refpanel: confirmacion a ojo
- Penguin Knight: confirmacion a ojo
- Ready for Intercepting: confirmacion a ojo
- Reasoning: confirmacion a ojo
- Riryoku: confirmacion a ojo
- Riryoku Field: confirmacion a ojo
- Seal of the Ancients: confirmacion a ojo
- Share the Pain: confirmacion a ojo
- The Inexperienced Spy: confirmacion a ojo
- Two-Pronged Attack: confirmacion a ojo
