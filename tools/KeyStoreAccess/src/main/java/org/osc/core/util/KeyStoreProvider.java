package org.osc.core.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.UnrecoverableEntryException;
import java.security.cert.CertificateException;
import java.security.spec.InvalidKeySpecException;
import java.util.Optional;

import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

/**
 * Singleton facade allowing to add/remove secrets from keystore
 */
public class KeyStoreProvider {
    // CONSTANTS
    public static String KEYSTORE_PASSWORD = "LNur%%PY9Bf&GQ+=n2^xP9BZAk*fuCHk";
    public static String KEYSTORE_PATH = "mainKeyStore.p12";
    private static final String SECRET_KEY_PASSWORD_ALGORITHM = "PBE";
    // SINGLETON CODE
    private KeyStoreProvider () throws KeyStoreProviderException{  }

    private static volatile KeyStoreProvider instance;

    public static KeyStoreProvider getInstance() throws KeyStoreProviderException{
        if (instance == null) {
            synchronized(KeyStoreProvider.class) {
                if(instance == null) {
                    instance = new KeyStoreProvider();
                    if(factory == null) {
                        factory = instance.new KeyStoreFromFileFactory();
                    }
                    instance.init();
                }
            }
        }

        return instance;
    }

    // KEY STORE INJECTION
    private static KeyStoreFactory factory = null;

    /**
     * Interface of factory method that create key store
     * Allows to replace the default keystore that is loaded from file
     */
    public interface KeyStoreFactory {
        KeyStore createKeyStore() throws KeyStoreProviderException;
        void persist(KeyStore keyStore) throws KeyStoreProviderException;
    }

    /**
     * Allows to inject the key store that is handled by provider.
     * This method has to be called before first .getInstance call
     * If no custom key store factory set - default one that loads
     * keystore from file is used
     * @param factory factory method that creates keystore
     */
    public static void setKeyStoreFactory(KeyStoreFactory factory) {
        KeyStoreProvider.factory = factory;
    }

    public class KeyStoreFromFileFactory implements KeyStoreFactory {

        @Override
        public KeyStore createKeyStore() throws KeyStoreProviderException {
            KeyStore keystore = null;

            System.out.println("Initializing keystore...");
            String keystorePassword = getKeyStorePassword();

            System.out.println("Opening keystore file....");
            try(InputStream keystoreStream = new FileInputStream(KEYSTORE_PATH)) {
                keystore = KeyStore.getInstance("PKCS12");
                System.out.println("Loading keystore from file....");
                keystore.load(keystoreStream, keystorePassword.toCharArray());
            } catch (IOException ioe) {
                throw new KeyStoreProviderException("Failed to obtain keystore from resources.", ioe);
            } catch (KeyStoreException kse) {
                throw new KeyStoreProviderException("Failed to create PKCS#12 keystore object.", kse);
            } catch (NoSuchAlgorithmException nsae) {
                throw new KeyStoreProviderException("Algorithm used to check the integrity of the keystore cannot be found.", nsae);
            } catch (CertificateException ce) {
                throw new KeyStoreProviderException("Certificates in the keystore could not be loaded.", ce);
            }

            return keystore;
        }

        @Override
        public void persist(KeyStore keyStore) throws KeyStoreProviderException {
            try(OutputStream keystoreOutputStream = getKeyStoreOutputStream()) {
                keyStore.store(keystoreOutputStream, getKeyStorePassword().toCharArray());
            } catch (KeyStoreException e) {
                throw new KeyStoreProviderException("Keystore has not been initialized or loaded", e);
            } catch (NoSuchAlgorithmException e) {
                throw new KeyStoreProviderException("The appropriate data integrity algorithm could not be found", e);
            } catch (CertificateException e) {
                throw new KeyStoreProviderException("Some of the certificates included in the keystore data could not be stored", e);
            } catch (IOException e) {
                throw new KeyStoreProviderException("Some I/O problem occured while storing keystore", e);
            }
        }

    }

    // MEMBERS
    private KeyStore keystore = null;

    // INNER TYPES
    public final class KeyStoreProviderException extends Exception {
        private static final long serialVersionUID = 6520829096189870519L;

        public KeyStoreProviderException(String message, Throwable cause) {
            super(message, cause);
        }

        public KeyStoreProviderException(String message) {
            super(message);
        }
    }

    private void init() throws KeyStoreProviderException {
        System.out.println("Initializing keystore...");
        this.keystore = factory.createKeyStore();
    }

    private String getKeyStorePassword() throws KeyStoreProviderException {
        return KEYSTORE_PASSWORD;
    }

    private OutputStream getKeyStoreOutputStream() throws KeyStoreProviderException {
        File file = new File(KEYSTORE_PATH);
        try {
            return new FileOutputStream(file);
        } catch (FileNotFoundException fnfe) {
            throw new KeyStoreProviderException("Keystore file not found in resources.", fnfe);

        }
    }

    /**
     * Gets the secret password stored in keystore under given alias.
     * @param alias
     * @param entryPassword entry password to access the secret password stored in keystore
     * @return the secret password or null if secret password does not exists in keystore
     * @throws KeyStoreProviderException
     */
    public String getPassword(String alias, String entryPassword) throws KeyStoreProviderException {
        try {
            System.out.println(String.format("Getting password with alias %s in keystore ...", alias));

            SecretKeyFactory factory = SecretKeyFactory.getInstance(SECRET_KEY_PASSWORD_ALGORITHM);

            Optional<KeyStore.SecretKeyEntry> ske = Optional.ofNullable((KeyStore.SecretKeyEntry) this.keystore.getEntry(alias, new KeyStore.PasswordProtection(entryPassword.toCharArray())));

            if(!ske.isPresent()) {
                return null;
            }

            PBEKeySpec keySpec = (PBEKeySpec)factory.getKeySpec(ske.get().getSecretKey(),PBEKeySpec.class);
            char[] password = keySpec.getPassword();

            if(password == null || password.length == 0) {
                throw new KeyStoreProviderException("Recovered password is blank.");
            }

            return new String(password);
        } catch (NoSuchAlgorithmException nsae) {
            throw new KeyStoreProviderException("Algorithm used to create PBE secret cannot be found.", nsae);
        } catch (UnrecoverableEntryException uee) {
            throw new KeyStoreProviderException("Invalid entry password to recover secret.", uee);
        } catch (KeyStoreException kse) {
            throw new KeyStoreProviderException("Failed to get PBE secret to keystore.", kse);
        } catch (InvalidKeySpecException ikse) {
            throw new KeyStoreProviderException("Failed to get key spec from PBE secret.", ikse);
        } catch (Exception e) {
            throw new KeyStoreProviderException("Failed to get PBE secret.", e);
        }
    }
}
