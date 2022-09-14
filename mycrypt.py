
class encrypt:   
    def string(ptext,key):
        ctext = ''
        last_letter = ''
        extended_key = ''
        for i in range(0,len(ptext),len(key)):
            extended_key += key
        for i,letter in enumerate(ptext):
            if last_letter == '':
                ctext += chr(ord(letter)+ord(extended_key[i]))
            else:
                ctext += chr(ord(letter)+ord(extended_key[i])+ord(last_letter)-ord(extended_key[i-1]))
            last_letter = letter
        return ctext

    def ceaser(ptext,key=14,caps=False):
        ctext = ''
        #start is exclusive, end is inclusive
        start,end = 96,122
        if caps:
            start,end = 64,90
            ptext = ptext.upper()
        else:
            ptext = ptext.lower()
        
        for letter in ptext:
            code = ord(letter) - start
            code += key
            if code>26:
                while code>26:
                    code-=26
            elif code<1:
                while code<1:
                    code+=26
            new_letter = chr(code + start)
            ctext += new_letter
        return ctext
        
    def filename(ptext,key,ceaserkey=14):
        ctext = ''
        extended_key = ''
        extension_len = 0
        for c in range(len(ptext)-1,-1,-1):
            if ptext[c] == '.':
                extension_len = len(ptext) - c - 1
                break
        for i in range(0,len(ptext),len(key)):
            extended_key += key
        for i,c in enumerate(ptext):
            if c != '.':
                c = encrypt.ceaser(c,ceaserkey + ord(extended_key[i]))
                ctext += c
            else:
                ctext += '.'
        return ctext
        

class decrypt: 
    def string(ctext,key):
        ptext = ''
        last_letter = ''
        extended_key = ''
        for i in range(0,len(ctext),len(key)):
            extended_key += key
        for i,letter in enumerate(ctext):
            if last_letter == '':
                ptext += chr(ord(letter)-ord(extended_key[i]))
            else:
                ptext += chr(ord(letter)-ord(extended_key[i])-(ord(last_letter)-ord(extended_key[i-1])))
            last_letter = ptext[i]
        return ptext

    def ceaser(ctext,key=14,caps=False):
        ptext = ''
        #start is exclusive, end is inclusive
        start,end = 96,122
        if caps:
            start,end = 64,90
            ctext = ctext.upper()
        else:
            ctext = ctext.lower()
        
        for letter in ctext:
            code = ord(letter) - start
            code -= key
            if code>26:
                while code>26:
                    code-=26
            elif code<1:
                while code<1:
                    code+=26
            new_letter = chr(code + start)
            ptext += new_letter
        return ptext

    def filename(ctext,key,ceaserkey=14):
        ptext = ''
        extended_key = ''
        extension_len = 0
        for c in range(len(ptext)-1,-1,-1):
            if ctext[c] == '.':
                extension_len = len(ctext) - c - 1
                break
        for i in range(0,len(ctext),len(key)):
            extended_key += key
        for i,c in enumerate(ctext):
            if c != '.':
                c = decrypt.ceaser(c,ceaserkey + ord(extended_key[i]))
                ptext += c
            else:
                ptext += '.'
        return ptext

if __name__ == '__main__':
    key = 'ayush'
    text = '1001000player'
    ctext = encrypt.string(text,key)
    ptext = decrypt.string(ctext,key)
    print(text)
    print(ctext)
    print(ptext)
    text = 'abCdEFGHi'
    ctext = encrypt.ceaser(text,93,True)
    ptext = decrypt.ceaser(ctext,93,False)
    print(text)
    print(ctext)
    print(ptext)
    text = 'apple.jpg'
    ctext = encrypt.filename(text,'ayush',7)
    ptext = decrypt.filename(ctext,'ayush',7)
    print(text)
    print(ctext)
    print(ptext)
