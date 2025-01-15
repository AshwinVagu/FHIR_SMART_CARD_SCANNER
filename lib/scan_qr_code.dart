import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ScanQrCode extends StatefulWidget {
  const ScanQrCode({super.key});

  @override
  State<ScanQrCode> createState() => _ScanQrCodeState();
}

class _ScanQrCodeState extends State<ScanQrCode> {
  String qrResult = 'Scanned Data will appear here';
  bool isLoading = false;

  Future<void> scanQR()async{
    try{
      final qrCode = await FlutterBarcodeScanner.scanBarcode('#ff6666', 'Cancel', true, ScanMode.QR);
      if(!mounted){
        return;
      }
        if(qrCode.toString().contains("shc:/")){
          final url = Uri.parse('https://fhir-smart-card-scanner.onrender.com/qr-decoding'); // Example API endpoint
          final headers = {'Content-Type': 'application/json'};
          final payload = {
            'qr_result': qrCode.toString()
          };
          try {
            setState(() {
              isLoading = true;
            });
            final response = await http.post(
              url,
              headers: headers,
              body: json.encode(payload), // Convert the payload to JSON
            );
            setState(() {
              isLoading = false;
              if (response.statusCode == 201) {
                final final_body = json.decode(response.body);
                String medical_entries = "";
                final entries = final_body['result'][1]['vc']['credentialSubject']['fhirBundle']['entry'];
                for (var entry in entries.asMap().entries) {
                  if(entry.key!=0){
                    medical_entries = medical_entries + json.encode(entry.value) + '\n';
                  }
                }
                this.qrResult = "Name details: ${entries[0]['resource']['name']} \n Type: ${entries[0]['resource']['resourceType']} \n Medical Entries: ${medical_entries} \n Verified: ${final_body['verified'].toString()}";
              } else {
                this.qrResult = "Failed to get data";
              }
            });
          } catch (e) {
            print('Error occurred: $e');
            setState(() {
              isLoading = false;
              this.qrResult = "Failed to get data";
            });
          }
        }
        else{
          setState(() {
            this.qrResult = "Not a smart card associated QR.";
          });
        }


    }on PlatformException{
      qrResult = 'Failed to read QR code';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('QR Code scanner')),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(height: 30,),
            Container(
                margin: EdgeInsets.all(16.0),
                child: Text('$qrResult',style: TextStyle(color: Colors.black),)
            ),
            SizedBox(height: 30,),
            ElevatedButton(onPressed: scanQR, child: Text('Scan Code')),
            if(isLoading) CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Colors.black), // Spinner color
              strokeWidth: 6.0,
            )
          ],
        ),
        )
      ),
    );
  }
}
