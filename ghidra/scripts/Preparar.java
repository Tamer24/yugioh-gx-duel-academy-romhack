// Prepara el programa: modo Thumb en todo el codigo y funciones con nombre.
// Argumento 1: ruta a nombres_yugiohgx-da.json ({"0x08XXXXXX": "nombre", ...}).
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSpace;
import ghidra.program.model.lang.Register;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;

import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Preparar extends GhidraScript {
    private static final long BASE = 0x08000000L;

    @Override
    public void run() throws Exception {
        String ruta = getScriptArgs()[0];
        AddressSpace sp = currentProgram.getAddressFactory().getDefaultAddressSpace();
        Register tmode = currentProgram.getLanguage().getRegister("TMode");
        currentProgram.getProgramContext().setValue(
            tmode, currentProgram.getMinAddress(), currentProgram.getMaxAddress(), BigInteger.ONE);

        String txt = new String(Files.readAllBytes(Paths.get(ruta)));
        Matcher m = Pattern.compile("\"0x([0-9A-Fa-f]{8})\"\\s*:\\s*\"([^\"]+)\"").matcher(txt);
        int creadas = 0, nombradas = 0;
        while (m.find()) {
            long dir = Long.parseLong(m.group(1), 16) & ~1L;
            if (dir < BASE || dir > currentProgram.getMaxAddress().getOffset()) continue;
            Address ad = sp.getAddress(dir);
            disassemble(ad);
            Function f = getFunctionAt(ad);
            if (f == null) {
                f = createFunction(ad, null);
                if (f != null) creadas++;
            }
            String nombre = m.group(2);
            if (f != null && !nombre.startsWith("FUN_") && !nombre.startsWith("_entry")) {
                f.setName(nombre, SourceType.USER_DEFINED);
                nombradas++;
            }
        }
        println("Funciones creadas: " + creadas + ", nombradas: " + nombradas);
    }
}
