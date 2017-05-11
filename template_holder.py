#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:38:14 2017

@author: christopher
"""

def getInfoTemplateText():
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!--[if IE]><html xmlns="http://www.w3.org/1999/xhtml" class="ie-browser" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><![endif]-->
<!--[if !IE]><!-->
<html style="margin: 0;padding: 0;" xmlns="http://www.w3.org/1999/xhtml">
<!--<![endif]-->

<head>
   <!--[if gte mso 9]><xml>
     <o:OfficeDocumentSettings>
      <o:AllowPNG/>
      <o:PixelsPerInch>96</o:PixelsPerInch>
     </o:OfficeDocumentSettings>
    </xml><![endif]-->
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <meta name="viewport" content="width=device-width">
   <!--[if !mso]><!-->
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <!--<![endif]-->
   <title>Template Base</title>


   <style type="text/css" id="media-query">
      body {
         margin: 0;
         padding: 0;
      }

      table,
      tr,
      td {
         vertical-align: top;
         border-collapse: collapse;
      }

      .ie-browser table,
      .mso-container table {
         table-layout: fixed;
      }

      * {
         line-height: inherit;
      }

      a[x-apple-data-detectors=true] {
         color: inherit !important;
         text-decoration: none !important;
      }

      [owa] .img-container div,
      [owa] .img-container button {
         display: block !important;
      }

      [owa] .fullwidth button {
         width: 100% !important;
      }

      .ie-browser .col,
      [owa] .block-grid .col {
         display: table-cell;
         float: none !important;
         vertical-align: top;
      }

      .ie-browser .num12,
      .ie-browser .block-grid,
      [owa] .num12,
      [owa] .block-grid {
         width: 500px !important;
      }

      .ExternalClass,
      .ExternalClass p,
      .ExternalClass span,
      .ExternalClass font,
      .ExternalClass td,
      .ExternalClass div {
         line-height: 100%;
      }

      .ie-browser .mixed-two-up .num4,
      [owa] .mixed-two-up .num4 {
         width: 164px !important;
      }

      .ie-browser .mixed-two-up .num8,
      [owa] .mixed-two-up .num8 {
         width: 328px !important;
      }

      .ie-browser .block-grid.two-up .col,
      [owa] .block-grid.two-up .col {
         width: 250px !important;
      }

      .ie-browser .block-grid.three-up .col,
      [owa] .block-grid.three-up .col {
         width: 166px !important;
      }

      .ie-browser .block-grid.four-up .col,
      [owa] .block-grid.four-up .col {
         width: 125px !important;
      }

      .ie-browser .block-grid.five-up .col,
      [owa] .block-grid.five-up .col {
         width: 100px !important;
      }

      .ie-browser .block-grid.six-up .col,
      [owa] .block-grid.six-up .col {
         width: 83px !important;
      }

      .ie-browser .block-grid.seven-up .col,
      [owa] .block-grid.seven-up .col {
         width: 71px !important;
      }

      .ie-browser .block-grid.eight-up .col,
      [owa] .block-grid.eight-up .col {
         width: 62px !important;
      }

      .ie-browser .block-grid.nine-up .col,
      [owa] .block-grid.nine-up .col {
         width: 55px !important;
      }

      .ie-browser .block-grid.ten-up .col,
      [owa] .block-grid.ten-up .col {
         width: 50px !important;
      }

      .ie-browser .block-grid.eleven-up .col,
      [owa] .block-grid.eleven-up .col {
         width: 45px !important;
      }

      .ie-browser .block-grid.twelve-up .col,
      [owa] .block-grid.twelve-up .col {
         width: 41px !important;
      }

      @media only screen and (min-width: 520px) {
         .block-grid {
            width: 500px !important;
         }
         .block-grid .col {
            display: table-cell;
            Float: none !important;
            vertical-align: top;
         }
         .block-grid .col.num12 {
            width: 500px !important;
         }
         .block-grid.mixed-two-up .col.num4 {
            width: 164px !important;
         }
         .block-grid.mixed-two-up .col.num8 {
            width: 328px !important;
         }
         .block-grid.two-up .col {
            width: 250px !important;
         }
         .block-grid.three-up .col {
            width: 166px !important;
         }
         .block-grid.four-up .col {
            width: 125px !important;
         }
         .block-grid.five-up .col {
            width: 100px !important;
         }
         .block-grid.six-up .col {
            width: 83px !important;
         }
         .block-grid.seven-up .col {
            width: 71px !important;
         }
         .block-grid.eight-up .col {
            width: 62px !important;
         }
         .block-grid.nine-up .col {
            width: 55px !important;
         }
         .block-grid.ten-up .col {
            width: 50px !important;
         }
         .block-grid.eleven-up .col {
            width: 45px !important;
         }
         .block-grid.twelve-up .col {
            width: 41px !important;
         }
      }

      @media (max-width: 520px) {
         .block-grid,
         .col {
            min-width: 320px !important;
            max-width: 100% !important;
         }
         .block-grid {
            width: calc(100% - 40px) !important;
         }
         .col {
            width: 100% !important;
         }
         .col>div {
            margin: 0 auto;
         }
         img.fullwidth {
            max-width: 100% !important;
         }
      }
   </style>
</head>
<!--[if mso]>
<body class="mso-container" style="background-color:#FFFFFF;">
<![endif]-->
<!--[if !mso]><!-->

<body class="clean-body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #FFFFFF">
   <!--<![endif]-->
   <div class="nl-container" style="min-width: 320px;Margin: 0 auto;background-color: #FFFFFF">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #FFFFFF;"><![endif]-->

      <div style="background-color:#2C2D37;">
         <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid two-up">
            <div style="border-collapse: collapse;display: table;width: 100%;">
               <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#2C2D37;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

               <!--[if (mso)|(IE)]><td align="center" width="250" style=" width:250px; padding-right: 0px; padding-left: 0px; padding-top:20px; padding-bottom:5px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
               <div class="col num6" style="Float: left;max-width: 320px;min-width: 250px;width: 250px;width: calc(35250px - 7000%);background-color: transparent;">
                  <div style="background-color: transparent; width: 100% !important;">
                     <!--[if (!mso)&(!IE)]><!-->
                     <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:20px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
                        <!--<![endif]-->


                        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                              <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center"><span style="font-size: 36px; line-height: 43px; color: rgb(255, 102, 0);">IAD</span></p>
                           </div>
                        </div>
                        <!--[if mso]></td></tr></table><![endif]-->


                        <!--[if (!mso)&(!IE)]><!-->
                     </div>
                     <!--<![endif]-->
                  </div>
               </div>
               <!--[if (mso)|(IE)]></td><td align="center" width="250" style=" width:250px; padding-right: 0px; padding-left: 0px; padding-top:20px; padding-bottom:20px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
               <div class="col num6" style="Float: left;max-width: 320px;min-width: 250px;width: 250px;width: calc(35250px - 7000%);background-color: transparent;">
                  <div style="background-color: transparent; width: 100% !important;">
                     <!--[if (!mso)&(!IE)]><!-->
                     <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:20px; padding-bottom:20px; padding-right: 0px; padding-left: 0px;">
                        <!--<![endif]-->


                        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 20px; padding-bottom: 20px;"><![endif]-->
                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 20px; padding-bottom: 20px;">
                           <div style="font-size:12px;line-height:18px;color:#6E6F7A;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                              <p style="margin: 0;font-size: 12px;line-height: 18px;text-align: center"><span style="font-size: 14px; line-height: 21px;">Algorithmen und Datenstrukturen </span></p>
                              <p style="margin: 0;font-size: 12px;line-height: 18px;text-align: center"><span style="font-size: 14px; line-height: 21px;">( SS 2017)</span></p>
                           </div>
                        </div>
                        <!--[if mso]></td></tr></table><![endif]-->


                        <!--[if (!mso)&(!IE)]><!-->
                     </div>
                     <!--<![endif]-->
                  </div>
               </div>
               <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
            </div>
         </div>
      </div>
      <div style="background-color:#323341;">
         <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid ">
            <div style="border-collapse: collapse;display: table;width: 100%;">
               <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#323341;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

               <!--[if (mso)|(IE)]><td align="center" width="500" style=" width:500px; padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
               <div class="col num12" style="min-width: 320px;max-width: 500px;width: 500px;width: calc(18000% - 89500px);background-color: transparent;">
                  <div style="background-color: transparent; width: 100% !important;">
                     <!--[if (!mso)&(!IE)]><!-->
                     <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
                        <!--<![endif]-->


                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                           <div align="center">
                              <div style="border-top: 10px solid transparent; width:100%;">&nbsp;</div>
                           </div>
                           <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                        </div>



                        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                              <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center"><span style="color: rgb(255, 255, 255); font-size: 28px; line-height: 33px;"><strong><span style="line-height: 33px; font-size: 28px;">VID:=SUBJECT</span></strong>
                                 </span>
                              </p>
                           </div>
                        </div>
                        <!--[if mso]></td></tr></table><![endif]-->



                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                           <div align="center">
                              <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                           </div>
                           <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                        </div>



                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                           <div align="center">
                              <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                           </div>
                           <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                        </div>



                        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                              <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: left"><span style="color: rgb(255, 255, 255); font-size: 20px; line-height: 24px;">VID:=GLOBAL_TEXT</span></p>
                           </div>
                        </div>
                        <!--[if mso]></td></tr></table><![endif]-->



                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                           <div align="center">
                              <div style="border-top: 10px solid transparent; width:100%;">&nbsp;</div>
                           </div>
                           <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                        </div>


                        <!--[if (!mso)&(!IE)]><!-->
                     </div>
                     <!--<![endif]-->
                  </div>
               </div>
               <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
            </div>
         </div>
      </div>
      <div style="background-color:#61626F;">
         <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid ">
            <div style="border-collapse: collapse;display: table;width: 100%;">
               <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#61626F;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

               <!--[if (mso)|(IE)]><td align="center" width="500" style=" width:500px; padding-right: 0px; padding-left: 0px; padding-top:30px; padding-bottom:30px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
               <div class="col num12" style="min-width: 320px;max-width: 500px;width: 500px;width: calc(18000% - 89500px);background-color: transparent;">
                  <div style="background-color: transparent; width: 100% !important;">
                     <!--[if (!mso)&(!IE)]><!-->
                     <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:30px; padding-bottom:30px; padding-right: 0px; padding-left: 0px;">
                        <!--<![endif]-->


                        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                              <p style="margin: 0;font-size: 12px;line-height: 14px"><span style="font-size: 18px; line-height: 21px;"><span style="line-height: 21px; color: rgb(255, 255, 255); font-size: 18px;"><span style="line-height: 21px; font-size: 18px;" id="_mce_caret" data-mce-bogus="true"><span style="line-height: 21px; font-size: 18px;">﻿</span></span>Liebe
                                 Grüße,<br></span><span style="line-height: 21px; color: rgb(255, 255, 255); font-size: 18px;">VID:=ME_NAME</span></span>
                              </p>
                           </div>
                        </div>
                        <!--[if mso]></td></tr></table><![endif]-->



                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                           <div align="center">
                              <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                           </div>
                           <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                        </div>



                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                           <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                           <div align="center">
                              <div style="border-top: 0px solid transparent; width:100%;">&nbsp;</div>
                           </div>
                           <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                        </div>


                        <!--[if (!mso)&(!IE)]><!-->
                     </div>
                     <!--<![endif]-->
                  </div>
               </div>
               <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
            </div>
         </div>
      </div>
      <div style="background-color:#ffffff;">
         <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid ">
            <div style="border-collapse: collapse;display: table;width: 100%;">
               <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#ffffff;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

               <!--[if (mso)|(IE)]><td align="center" width="500" style=" width:500px; padding-right: 0px; padding-left: 0px; padding-top:30px; padding-bottom:30px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
               <div class="col num12" style="min-width: 320px;max-width: 500px;width: 500px;width: calc(18000% - 89500px);background-color: transparent;">
                  <div style="background-color: transparent; width: 100% !important;">
                     <!--[if (!mso)&(!IE)]><!-->
                     <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:30px; padding-bottom:30px; padding-right: 0px; padding-left: 0px;">
                        <!--<![endif]-->


                        <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 15px; padding-bottom: 10px;"><![endif]-->
                        <div style="padding-right: 10px; padding-left: 10px; padding-top: 15px; padding-bottom: 10px;">
                           <div style="font-size:12px;line-height:18px;color:#959595;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                              <p style="margin: 0;font-size: 12px;line-height: 18px">Dies ist eine automatisch generierte Mail. Bei Fragen könnt ihr gerne auf diese Mail antworten oder einfach eine Mail an <span style="text-decoration: underline; font-size: 12px; line-height: 18px; color: rgb(255, 102, 0);">VID:=ME_MAIL</span>                                 schreiben</p>
                           </div>
                        </div>
                        <!--[if mso]></td></tr></table><![endif]-->


                        <!--[if (!mso)&(!IE)]><!-->
                     </div>
                     <!--<![endif]-->
                  </div>
               </div>
               <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
            </div>
         </div>
      </div>
      <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
   </div>


</body>

</html>

""".replace(u'\ufeff', '')

def getReturnTemplateText():
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!--[if IE]><html xmlns="http://www.w3.org/1999/xhtml" class="ie-browser" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><![endif]-->
<!--[if !IE]><!-->
<html style="margin: 0;padding: 0;" xmlns="http://www.w3.org/1999/xhtml">
<!--<![endif]-->

<head>
    <!--[if gte mso 9]><xml>
     <o:OfficeDocumentSettings>
      <o:AllowPNG/>
      <o:PixelsPerInch>96</o:PixelsPerInch>
     </o:OfficeDocumentSettings>
    </xml><![endif]-->
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width">
    <!--[if !mso]><!-->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!--<![endif]-->
    <title>Template Base</title>


    <style type="text/css" id="media-query">
        body {
            margin: 0;
            padding: 0;
        }

        table,
        tr,
        td {
            vertical-align: top;
            border-collapse: collapse;
        }

        .ie-browser table,
        .mso-container table {
            table-layout: fixed;
        }

        * {
            line-height: inherit;
        }

        a[x-apple-data-detectors=true] {
            color: inherit !important;
            text-decoration: none !important;
        }

        [owa] .img-container div,
        [owa] .img-container button {
            display: block !important;
        }

        [owa] .fullwidth button {
            width: 100% !important;
        }

        .ie-browser .col,
        [owa] .block-grid .col {
            display: table-cell;
            float: none !important;
            vertical-align: top;
        }

        .ie-browser .num12,
        .ie-browser .block-grid,
        [owa] .num12,
        [owa] .block-grid {
            width: 500px !important;
        }

        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {
            line-height: 100%;
        }

        .ie-browser .mixed-two-up .num4,
        [owa] .mixed-two-up .num4 {
            width: 164px !important;
        }

        .ie-browser .mixed-two-up .num8,
        [owa] .mixed-two-up .num8 {
            width: 328px !important;
        }

        .ie-browser .block-grid.two-up .col,
        [owa] .block-grid.two-up .col {
            width: 250px !important;
        }

        .ie-browser .block-grid.three-up .col,
        [owa] .block-grid.three-up .col {
            width: 166px !important;
        }

        .ie-browser .block-grid.four-up .col,
        [owa] .block-grid.four-up .col {
            width: 125px !important;
        }

        .ie-browser .block-grid.five-up .col,
        [owa] .block-grid.five-up .col {
            width: 100px !important;
        }

        .ie-browser .block-grid.six-up .col,
        [owa] .block-grid.six-up .col {
            width: 83px !important;
        }

        .ie-browser .block-grid.seven-up .col,
        [owa] .block-grid.seven-up .col {
            width: 71px !important;
        }

        .ie-browser .block-grid.eight-up .col,
        [owa] .block-grid.eight-up .col {
            width: 62px !important;
        }

        .ie-browser .block-grid.nine-up .col,
        [owa] .block-grid.nine-up .col {
            width: 55px !important;
        }

        .ie-browser .block-grid.ten-up .col,
        [owa] .block-grid.ten-up .col {
            width: 50px !important;
        }

        .ie-browser .block-grid.eleven-up .col,
        [owa] .block-grid.eleven-up .col {
            width: 45px !important;
        }

        .ie-browser .block-grid.twelve-up .col,
        [owa] .block-grid.twelve-up .col {
            width: 41px !important;
        }

        @media only screen and (min-width: 520px) {
            .block-grid {
                width: 500px !important;
            }
            .block-grid .col {
                display: table-cell;
                Float: none !important;
                vertical-align: top;
            }
            .block-grid .col.num12 {
                width: 500px !important;
            }
            .block-grid.mixed-two-up .col.num4 {
                width: 164px !important;
            }
            .block-grid.mixed-two-up .col.num8 {
                width: 328px !important;
            }
            .block-grid.two-up .col {
                width: 250px !important;
            }
            .block-grid.three-up .col {
                width: 166px !important;
            }
            .block-grid.four-up .col {
                width: 125px !important;
            }
            .block-grid.five-up .col {
                width: 100px !important;
            }
            .block-grid.six-up .col {
                width: 83px !important;
            }
            .block-grid.seven-up .col {
                width: 71px !important;
            }
            .block-grid.eight-up .col {
                width: 62px !important;
            }
            .block-grid.nine-up .col {
                width: 55px !important;
            }
            .block-grid.ten-up .col {
                width: 50px !important;
            }
            .block-grid.eleven-up .col {
                width: 45px !important;
            }
            .block-grid.twelve-up .col {
                width: 41px !important;
            }
        }

        @media (max-width: 520px) {
            .block-grid,
            .col {
                min-width: 320px !important;
                max-width: 100% !important;
            }
            .block-grid {
                width: calc(100% - 40px) !important;
            }
            .col {
                width: 100% !important;
            }
            .col>div {
                margin: 0 auto;
            }
            img.fullwidth {
                max-width: 100% !important;
            }
        }
    </style>
</head>
<!--[if mso]>
<body class="mso-container" style="background-color:#FFFFFF;">
<![endif]-->
<!--[if !mso]><!-->

<body class="clean-body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #FFFFFF">
    <!--<![endif]-->
    <div class="nl-container" style="min-width: 320px;Margin: 0 auto;background-color: #FFFFFF">
        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #FFFFFF;"><![endif]-->

        <div style="background-color:#2C2D37;">
            <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid two-up">
                <div style="border-collapse: collapse;display: table;width: 100%;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#2C2D37;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

                    <!--[if (mso)|(IE)]><td align="center" width="250" style=" width:250px; padding-right: 0px; padding-left: 0px; padding-top:20px; padding-bottom:5px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
                    <div class="col num6" style="Float: left;max-width: 320px;min-width: 250px;width: 250px;width: calc(35250px - 7000%);background-color: transparent;">
                        <div style="background-color: transparent; width: 100% !important;">
                            <!--[if (!mso)&(!IE)]><!-->
                            <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:20px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
                                <!--<![endif]-->


                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center"><span style="font-size: 36px; line-height: 43px; color: rgb(255, 102, 0);">IAD</span></p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->


                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                        </div>
                    </div>
                    <!--[if (mso)|(IE)]></td><td align="center" width="250" style=" width:250px; padding-right: 0px; padding-left: 0px; padding-top:20px; padding-bottom:20px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
                    <div class="col num6" style="Float: left;max-width: 320px;min-width: 250px;width: 250px;width: calc(35250px - 7000%);background-color: transparent;">
                        <div style="background-color: transparent; width: 100% !important;">
                            <!--[if (!mso)&(!IE)]><!-->
                            <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:20px; padding-bottom:20px; padding-right: 0px; padding-left: 0px;">
                                <!--<![endif]-->


                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 20px; padding-bottom: 20px;"><![endif]-->
                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 20px; padding-bottom: 20px;">
                                    <div style="font-size:12px;line-height:18px;color:#6E6F7A;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 12px;line-height: 18px;text-align: center"><span style="font-size: 14px; line-height: 21px;">Algorithmen und Datenstrukturen </span></p>
                                        <p style="margin: 0;font-size: 12px;line-height: 18px;text-align: center"><span style="font-size: 14px; line-height: 21px;">( SS 2017)</span></p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->


                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                        </div>
                    </div>
                    <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                </div>
            </div>
        </div>
        <div style="background-color:#323341;">
            <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid ">
                <div style="border-collapse: collapse;display: table;width: 100%;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#323341;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

                    <!--[if (mso)|(IE)]><td align="center" width="500" style=" width:500px; padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
                    <div class="col num12" style="min-width: 320px;max-width: 500px;width: 500px;width: calc(18000% - 89500px);background-color: transparent;">
                        <div style="background-color: transparent; width: 100% !important;">
                            <!--[if (!mso)&(!IE)]><!-->
                            <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
                                <!--<![endif]-->


                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 10px solid transparent; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>



                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 12px;line-height: 14px;text-align: center"><span style="color: rgb(255, 255, 255); font-size: 28px; line-height: 33px;"><strong><span style="line-height: 33px; font-size: 28px;"><span style="line-height: 33px; font-size: 28px;"></span>Blatt VID:=B_NUMMER</span>
                                            </strong>
                                            </span>
                                        </p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>



                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top: 30px; padding-bottom: 30px;"><![endif]-->
                                <div style="padding-right: 0px; padding-left: 0px; padding-top: 30px; padding-bottom: 30px;">
                                    <div style="font-size:12px;line-height:14px;color:#ffffff;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: center"><span style="font-size: 22px; line-height: 26px; color: rgb(153, 153, 153);"><strong><span style="line-height: 26px; font-size: 22px;">An alle Teilnehmer:</span></strong>
                                            </span>
                                        </p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>



                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: left"><span style="color: rgb(255, 255, 255); font-size: 18px; line-height: 21px;">VID:=GLOBAL_TEXT</span></p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 10px solid transparent; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>


                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                        </div>
                    </div>
                    <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                </div>
            </div>
        </div>
        <div style="background-color:#61626F;">
            <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid ">
                <div style="border-collapse: collapse;display: table;width: 100%;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#61626F;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

                    <!--[if (mso)|(IE)]><td align="center" width="500" style=" width:500px; padding-right: 0px; padding-left: 0px; padding-top:30px; padding-bottom:30px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
                    <div class="col num12" style="min-width: 320px;max-width: 500px;width: 500px;width: calc(18000% - 89500px);background-color: transparent;">
                        <div style="background-color: transparent; width: 100% !important;">
                            <!--[if (!mso)&(!IE)]><!-->
                            <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:30px; padding-bottom:30px; padding-right: 0px; padding-left: 0px;">
                                <!--<![endif]-->


                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top: 30px; padding-bottom: 30px;"><![endif]-->
                                <div style="padding-right: 0px; padding-left: 0px; padding-top: 30px; padding-bottom: 30px;">
                                    <div style="font-size:12px;line-height:14px;color:#ffffff;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: center"><span style="font-size: 22px; line-height: 26px; color: rgb(255, 153, 0);"><strong><span style="line-height: 26px; font-size: 22px;">Persönliches Feedback an:</span></strong>
                                            </span>
                                        </p>
                                        <p style="margin: 0;font-size: 14px;line-height: 16px;text-align: center"><span style="font-size: 22px; line-height: 26px; color: rgb(255, 153, 0);"><strong><span style="line-height: 26px; font-size: 22px;">VID:=MEMBER_NAMES</span></strong>
                                            </span>
                                        </p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>

                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <table border="1" style="width: 100%; border-collapse: collapse; font-size:20px; line-height:30px; color:#FFFFFF; font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <tr>
                                            VID:=HTML_TH_EX
                                            <th style="text-align: center;">&sum;</th>
                                        </tr>
                                        <tr>
                                            VID:=HTML_TD_P
                                            <td style="text-align: center;">VID:=P_SUM</td>
                                        </tr>
                                    </table>
                                </div>


                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><![endif]-->
                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 14px;line-height: 17px;text-align: left"><span style="color: rgb(255, 255, 255); font-size: 18px; line-height: 21px;">VID:=LOCAL_FEEDBACK</span></p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 0px solid transparent; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>



                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                    <!--[if (mso)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px;padding-left: 10px; padding-top: 10px; padding-bottom: 10px;"><table width="100%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
                                    <div align="center">
                                        <div style="border-top: 1px solid #BBBBBB; width:100%;">&nbsp;</div>
                                    </div>
                                    <!--[if (mso)]></td></tr></table></td></tr></table><![endif]-->
                                </div>

                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 10px;">
                                   <div style="font-size:12px;line-height:14px;color:#555555;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                      <p style="margin: 0;font-size: 12px;line-height: 14px"><span style="font-size: 18px; line-height: 21px;"><span style="line-height: 21px; color: rgb(255, 255, 255); font-size: 18px;"><span style="line-height: 21px; font-size: 18px;" id="_mce_caret" data-mce-bogus="true"><span style="line-height: 21px; font-size: 18px;">﻿</span></span>Liebe
                                         Grüße,<br></span><span style="line-height: 21px; color: rgb(255, 255, 255); font-size: 18px;">VID:=ME_NAME</span></span>
                                      </p>
                                   </div>
                                </div>
                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                        </div>
                    </div>
                    <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                </div>
            </div>
        </div>
        <div style="background-color:#ffffff;">
            <div style="Margin: 0 auto;min-width: 320px;max-width: 500px;width: 500px;width: calc(19000% - 98300px);overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;" class="block-grid ">
                <div style="border-collapse: collapse;display: table;width: 100%;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#ffffff;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width: 500px;"><tr class="layout-full-width" style="background-color:transparent;"><![endif]-->

                    <!--[if (mso)|(IE)]><td align="center" width="500" style=" width:500px; padding-right: 0px; padding-left: 0px; padding-top:30px; padding-bottom:30px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><![endif]-->
                    <div class="col num12" style="min-width: 320px;max-width: 500px;width: 500px;width: calc(18000% - 89500px);background-color: transparent;">
                        <div style="background-color: transparent; width: 100% !important;">
                            <!--[if (!mso)&(!IE)]><!-->
                            <div style="border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent; padding-top:30px; padding-bottom:30px; padding-right: 0px; padding-left: 0px;">
                                <!--<![endif]-->


                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 15px; padding-bottom: 10px;"><![endif]-->
                                <div style="padding-right: 10px; padding-left: 10px; padding-top: 15px; padding-bottom: 10px;">
                                    <div style="font-size:12px;line-height:18px;color:#959595;font-family:Arial, 'Helvetica Neue', Helvetica, sans-serif;text-align:left;">
                                        <p style="margin: 0;font-size: 12px;line-height: 18px">Dies ist eine automatisch generierte Mail. Bei Fragen könnt ihr gerne auf diese Mail antworten oder einfach eine Mail an <span style="text-decoration: underline; font-size: 12px; line-height: 18px; color: rgb(255, 102, 0);">VID:=ME_MAIL</span>                                            schreiben</p>
                                    </div>
                                </div>
                                <!--[if mso]></td></tr></table><![endif]-->


                                <!--[if (!mso)&(!IE)]><!-->
                            </div>
                            <!--<![endif]-->
                        </div>
                    </div>
                    <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                </div>
            </div>
        </div>
        <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
    </div>


</body>

</html>
""".replace(u'\ufeff', '')

