import time
from anticaptchaofficial.recaptchav2proxyless import AntiCaptchaRecaptchaV2Proxyless

# Your Anti-Captcha API key
# https://anti-captcha.com/
API_KEY = 'YOUR_ANTI_CAPTCHA_API_KEY'



def solve_captcha(site_url, site_key):
    """
    Solves reCAPTCHA using Anti-Captcha service.

    :param site_url: The URL of the page containing the CAPTCHA.
    :param site_key: The site key for the CAPTCHA.
    :return: The solution to the CAPTCHA.
    """
    solver = AntiCaptchaRecaptchaV2Proxyless()
    
    # Set your Anti-Captcha API key
    solver.set_key(API_KEY)
    
    # Set the target website URL and CAPTCHA site key
    solver.set_website_url(site_url)
    solver.set_website_key(site_key)
    
    # Solve CAPTCHA
    response = solver.solve_and_return_solution()
    
    if response != 0:
        print(f"CAPTCHA solved: {response}")
        return response
    else:
        print(f"Error solving CAPTCHA: {solver.error_code}")
        return None
