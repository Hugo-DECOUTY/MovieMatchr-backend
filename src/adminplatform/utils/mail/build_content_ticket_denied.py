import base64
import os
from dotenv import load_dotenv
from adminplatform.utils.emailStyle.email_style import EMAIL_STYLE

load_dotenv()

MICROPORT_CRM_LOGO = os.getenv("MICROPORT_CRM_LOGO")
SUPPORT_CONTACT = os.getenv("SUPPORT_CONTACT")


async def build_content_ticket_denied(
    name: str,
    email: str,
    body: str,
):

    with open(str(MICROPORT_CRM_LOGO), "rb") as file:
        microport_crm_logo = base64.b64encode(file.read()).decode("utf-8")

    return f"""\
    <!DOCTYPE html>
        <html lang="fr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
        {EMAIL_STYLE}
        <!--
            The email background color is defined in three places, just below. If you change one, remember to change the others.
            1. body tag: for most email clients
            2. center tag: for Gmail and Inbox mobile apps and web versions of Gmail, GSuite, Inbox, Yahoo, AOL, Libero, Comcast, freenet, Mail.ru, Orange.fr
            3. mso conditional: For Windows 10 Mail
        -->
        <body width="100%" style="margin: 0; padding: 0 !important; background: #f3f3f5; mso-line-height-rule: exactly;">
            <center style="width: 100%; background: #f3f3f5;">
            <!--[if mso | IE]>
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f3f3f5;">
            <tr>
            <td>
            <![endif]-->

                <!-- Visually Hidden Preview Text : BEGIN -->
                <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
                    Ticket Denied
                </div>
                <!-- Visually Hidden Preview Text : END -->

                <div class="email-container" style="max-width: 680px; margin: 0 auto;">
                    <!--[if mso]>
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="680" align="center">
                    <tr>
                    <td>
                    <![endif]-->
                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="max-width: 680px; width:100%">
                        <!-- Logo : BEGIN -->
                        <tr>
                            <td style="padding: 20px 30px; text-align: left;" class="sm-px">
                                <img src="data:image/png;base64, {microport_crm_logo}" alt="Microport CRM logo." border="0" width="240" height="75" style="display: block; font-family: arial, sans-serif; font-size: 15px; line-height: 15px; color: #3C3F44; margin: 0;">
                            </td>
                        </tr>
                        <!-- Logo : END -->

                        <!-----------------------------

                            EMAIL BODY : BEGIN

                        ------------------------------>

                        <tr>
                            <td style="padding: 30px; background-color: #ffffff;" class="sm-p bar">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                                    <!-- Rich Text : BEGIN -->
                                    <tr>
                                        <td style="padding-bottom: 15px; font-family: arial, sans-serif; font-size: 15px; line-height: 21px; color: #3C3F44; text-align: left;">
                                            
                                            <h1 style="font-weight: bold; font-size: 20px; line-height: 20px; color: #0C0D0E; margin: 0 0 15px 0;">
                                                Ticket denied
                                            </h1>

                                            <p style="margin: 0 0 15px;">
                                                Hello {name} !
                                            </p>

                                            <p style="margin: 0 0 15px;">
                                                Your request has been denied for the following reason:
                                            </p>

                                            <p style="margin: 0 0 15px;">
                                                {body}
                                            </p>

                                            <p style="margin: 0 0 15px;">
                                                Please contact us at <a href="mailto:{SUPPORT_CONTACT}">{SUPPORT_CONTACT}</a>
                                            </p>

                                            <p style="margin: 0 0 15px;">
                                                The Microport Team
                                            </p>

                                        </td>
                                    </tr>
                                    <!-- Rich Text : END -->
                                </table>
                            </td>
                        </tr>

                        <!-----------------------------

                            EMAIL BODY : END

                        ------------------------------>

                    </table>
                </div>
            <!--[if mso | IE]>
            </td>
            </tr>
            </table>
            <![endif]-->
            </center>
        </body>
        </html>"""