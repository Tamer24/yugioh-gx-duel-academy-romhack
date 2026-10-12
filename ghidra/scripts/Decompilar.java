// Decompila funciones y vuelca el C a un archivo.
// Argumentos: salida.c dir1 [dir2 ...]   (direcciones en hexadecimal, p. ej. 080577E8)
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

import java.io.PrintWriter;

public class Decompilar extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        DecompInterface di = new DecompInterface();
        di.openProgram(currentProgram);
        // En un ROM de juego ninguna funcion "no retorna": Ghidra lo dedujo mal para varias
        // (FUN_0800e158, ask_question, send_card_to_graveyard...) y el decompilado se cortaba
        // en la primera llamada. Se quita la marca a todas antes de decompilar.
        for (Function g : currentProgram.getFunctionManager().getFunctions(true)) {
            if (g.hasNoReturn()) g.setNoReturn(false);
        }
        try (PrintWriter out = new PrintWriter(a[0])) {
            for (int i = 1; i < a.length; i++) {
                Address ad = toAddr(Long.parseLong(a[i], 16) & ~1L);
                Function f = getFunctionAt(ad);
                if (f == null) f = createFunction(ad, null);
                out.println("// ===== " + a[i] + (f != null ? " " + f.getName() : " (sin funcion)"));
                if (f == null) continue;
                DecompileResults r = di.decompileFunction(f, 90, monitor);
                out.println(r.decompileCompleted() ? r.getDecompiledFunction().getC() : "// error: " + r.getErrorMessage());
            }
        }
        di.dispose();
    }
}
