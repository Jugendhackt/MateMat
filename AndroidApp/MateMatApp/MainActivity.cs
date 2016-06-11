using System;
using Android.App;
using Android.Content;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using Android.OS;
using System.Net;
using Android.Graphics;

namespace MateMatApp
{
    [Activity(Label = "MateMatApp", MainLauncher = true, Icon = "@drawable/icon")]
    public class MainActivity : Activity
    {
        //VERBUGGTE VERSION
        
        //Diese Version hat keine Fehler im Code (Auch meinung von Mentoren)
        //Es gibt einen License Fehler der ohne Grund aufgetaucht ist!
        //Auch in älteren, sogar den ersten versionen der App taucht er plötzlich
        //auf.
        
        int profID = 0000;
        string qr_code_link;

        protected override void OnCreate(Bundle bundle)
        {
            base.OnCreate(bundle);

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.Main);

            //link gen
            Button codeGenButton = FindViewById<Button>(Resource.Id.genCode);
            EditText ProfnumberText = FindViewById<EditText>(Resource.Id.code_text);

            codeGenButton.Click += (object sender, EventArgs e) =>
            {
                //Konvertiert String to Ints
                profID = Convert.ToInt32(ProfnumberText.Text);

                //Generiert Code
                qr_code_link = "https://api.qrserver.com/v1/create-qr-code/?data=" + profID + "&size=256x256";

                //Setz image ein
                qrcode_v = FindViewById<ImageView>(Resource.Id.qrcode_view);
                var imageBitmap = GetImageBitmapFromUrl(qr_code_link);
                qrcode_v.SetImageBitmap(imageBitmap);
            };
        }

        private ImageView qrcode_v;

        //ImageBitMap Image Download
        //Source: http://goo.gl/Vmddut
        private Bitmap GetImageBitmapFromUrl(string url)
        {
            Bitmap imageBitmap = null;

            using (var webClient = new WebClient())
            {
                var imageBytes = webClient.DownloadData(url);
                if (imageBytes != null && imageBytes.Length > 0)
                {
                    imageBitmap = BitmapFactory.DecodeByteArray(imageBytes, 0, imageBytes.Length);
                }
            }
            return imageBitmap;
        }
    }
}

