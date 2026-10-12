"""Crea un parche BPS minimo (compatible con Flips y RomPatcher.js).

IPS no sirve para este juego: no puede direccionar mas alla de 16 MB y casi
todos los datos interesantes estan despues.

Uso: python3 bps.py original.gba modificado.gba parche.bps
     python3 bps.py --aplicar original.gba parche.bps salida.gba
"""
import sys
import zlib


def _num(n):
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if n == 0:
            out.append(0x80 | x)
            return bytes(out)
        out.append(x)
        n -= 1


def crear(src, dst):
    assert len(src) == len(dst), "este creador solo soporta ROMs del mismo tamano"
    out = bytearray(b"BPS1") + _num(len(src)) + _num(len(dst)) + _num(0)
    i, n = 0, len(dst)
    while i < n:
        j = i
        if src[i] == dst[i]:
            while j < n and src[j] == dst[j]:
                j += 1
            out += _num(((j - i - 1) << 2) | 0)          # SourceRead
        else:
            # junta diferencias separadas por menos de 8 bytes iguales
            while j < n:
                if src[j] != dst[j]:
                    j += 1
                    continue
                k = j
                while k < n and k - j < 8 and src[k] == dst[k]:
                    k += 1
                if k < n and k - j < 8:
                    j = k
                else:
                    break
            out += _num(((j - i - 1) << 2) | 1) + dst[i:j]  # TargetRead
        i = j
    for blob in (src, dst):
        out += (zlib.crc32(blob) & 0xFFFFFFFF).to_bytes(4, "little")
    out += (zlib.crc32(out) & 0xFFFFFFFF).to_bytes(4, "little")
    return bytes(out)


def aplicar(src, parche):
    """Aplicador de referencia, solo para verificar lo que genera crear()."""
    assert parche[:4] == b"BPS1"
    pos = 4

    def num():
        nonlocal pos
        data, shift = 0, 1
        while True:
            x = parche[pos]
            pos += 1
            data += (x & 0x7F) * shift
            if x & 0x80:
                return data
            shift <<= 7
            data += shift

    num(); tam = num(); meta = num(); pos += meta
    out = bytearray()
    while pos < len(parche) - 12:
        v = num()
        modo, largo = v & 3, (v >> 2) + 1
        if modo == 0:
            out += src[len(out):len(out) + largo]
        elif modo == 1:
            out += parche[pos:pos + largo]
            pos += largo
        else:
            raise ValueError("modo no soportado")
    assert len(out) == tam
    return bytes(out)


if __name__ == "__main__":
    if sys.argv[1] == "--aplicar":        # bps.py --aplicar original.gba parche.bps salida.gba
        a = open(sys.argv[2], "rb").read()
        p = open(sys.argv[3], "rb").read()
        assert zlib.crc32(a) & 0xFFFFFFFF == int.from_bytes(p[-12:-8], "little"), "el original no es el esperado"
        b = aplicar(a, p)
        assert zlib.crc32(b) & 0xFFFFFFFF == int.from_bytes(p[-8:-4], "little"), "el resultado no coincide"
        open(sys.argv[4], "wb").write(b)
        print(f"{sys.argv[4]}: {len(b)} bytes")
    else:
        a = open(sys.argv[1], "rb").read()
        b = open(sys.argv[2], "rb").read()
        p = crear(a, b)
        assert aplicar(a, p) == b
        open(sys.argv[3], "wb").write(p)
        print(f"{sys.argv[3]}: {len(p)} bytes")
