# TryHackMe Advent of Cyber - Day 19: I merely noticed that you’re improperly stored, my dear secret!

Glitch, the protagonist, is determined to expose the corrupt Mayor Malware. Upon reaching the Mayor's downtown office, Glitch encounters a smart lock controlled by an eerie game. To proceed, Glitch must use hacking skills to manipulate the game's logic.

## Learning Objectives
- Understand how to interact with an executable's API.
- Intercept and modify internal APIs using Frida.
- Hack a game with Frida.

## Key Concepts

### Game Hacking
The gaming industry, with its vast revenue, attracts attackers who exploit vulnerabilities for malicious purposes. Hacking games involves complex skills like memory management, reverse engineering, and networking.

### Executables and Libraries
- **Executables**: Standalone binary files with compiled code.
- **Libraries**: Reusable code collections with a ".so" extension, which applications call to perform operations.
- **Attack Vector**: Intercepting library function calls to alter arguments or return values, disrupting application behavior.

### Hacking with Frida
Frida is an instrumentation tool used for analyzing and interacting with applications in real-time. It creates a thread in the target process and allows JavaScript code injection to control the application's behavior. Key functionality includes:
- **Interceptor**: Alters inputs/outputs of internal functions or observes their behavior.
- **Hooks**: 
  - `onEnter`: Accesses function arguments.
  - `onLeave`: Accesses return values.

## Practical Application: Breaking the Game

### Initial Steps
1. Start the target game executable:
   ```bash
   cd /home/ubuntu/Desktop/TryUnlockMe && ./TryUnlockMe
   ```
2. Use Frida to trace library functions:
   ```bash
   frida-trace ./TryUnlockMe -i 'libaocgame.so!*'
   ```

### Level 1: OTP Manipulation
1. Identify the function `_Z7set_otpi`.
2. Hook the function using the generated handler script:
   ```javascript
   defineHandler({
     onEnter(log, args, state) {
       log('_Z7set_otpi()');
       log("Parameter:" + args[0].toInt32());
     },
     onLeave(log, retval, state) {}
   });
   ```
3. Extract the OTP parameter from the log and use it to pass the level.

### Level 2: Coin Manipulation
1. Identify the function `_Z17validate_purchaseiii`.
2. Inspect function parameters to identify item ID, price, and player's coin balance:
   ```javascript
   defineHandler({
     onEnter(log, args, state) {
       log('_Z17validate_purchaseiii()');
       log('PARAMETER 1: ' + args[0]);
       log('PARAMETER 2: ' + args[1]);
       log('PARAMETER 3: ' + args[2]);
     },
     onLeave(log, retval, state) {}
   });
   ```
3. Set the price parameter to zero to buy items without spending coins:
   ```javascript
   args[1] = ptr(0);
   ```

### Level 3: Biometrics Check
1. Identify the function `_Z16check_biometricsPKc()`.
2. Log the string parameter:
   ```javascript
   defineHandler({
     onEnter(log, args, state) {
       log('_Z16check_biometricsPKc()');
       log("PARAMETER:" + Memory.readCString(args[0]));
     },
     onLeave(log, retval, state) {}
   });
   ```
3. Log and modify the return value to trick the game into passing the check:
   ```javascript
   onLeave(log, retval, state) {
       log("The return value is: " + retval);
       retval.replace(ptr(1));
   }
   ```

## Questions

1. What is the OTP flag?
    >THM{one_tough_password}
2. What is the billionaire item flag?
    >THM{credit_card_undeclined}
3. What is the biometric flag?
    >THM{dont_smash_your_keyboard}