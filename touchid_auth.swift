import LocalAuthentication
import Foundation

let context = LAContext()
var error: NSError?

guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
    fputs("ERROR: Touch ID not available - \(error?.localizedDescription ?? "unknown")\n", stderr)
    exit(1)
}

let reason = "Claude Code の操作を許可するにはTouch IDで認証してください"
let semaphore = DispatchSemaphore(value: 0)
var authSuccess = false

context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { success, authError in
    if success {
        authSuccess = true
    } else {
        fputs("DENIED: Authentication failed - \(authError?.localizedDescription ?? "unknown")\n", stderr)
    }
    semaphore.signal()
}

semaphore.wait()
exit(authSuccess ? 0 : 1)
