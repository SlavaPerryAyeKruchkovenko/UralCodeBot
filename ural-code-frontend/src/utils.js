/**
 * Метод для дешифровки строки, зашифрованной с помощью ROT13
 * @param str - зашифрована строка, только заглавные буквы латинского алфавита
 * @returns {*} - расшифрован строка
 */
export function decodeROT13(str) {
    return str.replace(/[A-Za-z]/g, (char) => {
        const base = char <= 'Z' ? 65 : 97;
        return String.fromCharCode(((char.charCodeAt(0) - base + 13) % 26) + base);
    });
}

