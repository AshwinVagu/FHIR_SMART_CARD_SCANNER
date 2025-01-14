import base64
import json
import zlib

def decode_smart_health_card(shc_data):
    try:
        # Step 1: Remove the "shc:/" prefix
        if shc_data.startswith("shc:/"):
            shc_data = shc_data[5:]

        # Step 2: Convert the numeric string to ASCII
        pairs = [int(shc_data[i:i+2]) + 45 for i in range(0, len(shc_data), 2)]
        jws = ''.join(chr(pair) for pair in pairs)

        print("Decoded JWS String:", jws)  # Debugging: Check the JWS string

        # Step 3: Split the JWS into its components
        if jws.count('.') != 2:
            raise ValueError("Decoded data does not have a valid JWS structure")
        header, payload, signature = jws.split('.')

        # Step 4: Base64-decode the header and payload
        def base64_decode(data):
            """Helper function to decode base64 strings with padding."""
            padding = '=' * (4 - len(data) % 4)  # Add padding if necessary
            return base64.urlsafe_b64decode(data + padding)

        # Decode header
        header_json = json.loads(base64_decode(header).decode('utf-8'))
        print("Decoded Header:", json.dumps(header_json, indent=2))

        # Decode payload
        compressed_payload = base64_decode(payload)
        if header_json.get("zip") == "DEF":
            # Decompress payload if "zip" is "DEF"
            decompressed_payload = zlib.decompress(compressed_payload, wbits=-15)  # Raw DEFLATE
            payload_json = json.loads(decompressed_payload.decode('utf-8'))
        else:
            payload_json = json.loads(compressed_payload.decode('utf-8'))

        print("Decoded Payload:", json.dumps(payload_json, indent=2))
        return header_json, payload_json

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return None
    except Exception as e:
        print(f"Error decoding SMART Health Card: {e}")
        return None

# Example SMART Health Card data
# shc_data = "shc:/5676290952432060346029243740446031222959532654603460292540772804336028702864716745222809286233313440122732414562400344054542557144641272400355763227440733404145402667074225676639054177532611773803410442425460573601064531313970327424244350455560263524670829317022261136263640252268207343643952235028597029093058502373616720603658201158116444760476570677723633762772666620645912414242003822056426676840766211217266671025296733383758045972666067330843677733770710312127662904377224434471363543033871272259365225227474754300073467342874254406104362555255664154377629665059553105412154636921303623647003584438090912533530243403712665283552237762413521353206395865657510436365526641370712235377626354617345590603610554402152674558053456243572210465452730650431043931356007430040700022590020331274273107570876540339592259383924351067523105057372533063272405560772270454742669584326736077295460372437376372415943732221444059003323271005113941121165766262356575083809413758741068404340673121220472352126636932717337691250085827695062502122266542524269573307622077390640640075542676352464773529392625452320720300004259655874083312354504542276764065457253324274381228394470456761506511267361662774440064395211267359082174010844440776055650031066555977335733377271205352527623083853720544621211770534302663561132047765446635564053635368035429763143283821566412441059565557270574681225253165336074"
# decode_smart_health_card(shc_data)