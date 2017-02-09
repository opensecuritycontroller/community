package org.osc.core.util;

import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class Main {
    public static void main(String[] args) throws KeyStoreProvider.KeyStoreProviderException, FileNotFoundException {
        KeyStoreProvider.KEYSTORE_PASSWORD = "LNur%%PY9Bf&GQ+=n2^xP9BZAk*fuCHk";

        if(args.length == 1) {
            KeyStoreProvider.KEYSTORE_PATH = args[0]; //"mainKeyStore.p12";
        } else {
            System.err.println("Usage: KeyStoreAccess-1.0.jar <keystore path>");
            return;
        }


        String dbPassword = KeyStoreProvider.getInstance().getPassword("DB_PASSWORD", "pGszjP_6t&pbJcJqm@NFm@Qan7BPyDwB");
        System.out.println("DB PASSWORD:");
        System.out.println(dbPassword);
        try( PrintWriter out = new PrintWriter("db_password.txt") ){
            out.println( dbPassword );
            System.out.println("Stored in db_password.txt");
        }
    }
}
