import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
    
      body: Stack(
        children: [
          // --- 1. ΤΟ ΦΟΝΤΟ  ---
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.white,        
                  Color(0xFFE8F5E9),   
                ],
              ),
            ),
          ),

          // --- 2. ΔΙΑΚΟΣΜΗΤΙΚΟΙ ΚΥΚΛΟΙ  ---
          Positioned(
            top: -50,
            right: -50,
            child: Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                color: const Color(0xFF2E8B57).withOpacity(0.05), 
                shape: BoxShape.circle,
              ),
            ),
          ),
          Positioned(
            bottom: 100,
            left: -40,
            child: Container(
              width: 150,
              height: 150,
              decoration: BoxDecoration(
                color: Colors.orange.withOpacity(0.05), 
                shape: BoxShape.circle,
              ),
            ),
          ),

          // --- 3. ΤΟ ΠΕΡΙΕΧΟΜΕΝΟ (Κέντρο) ---
          Center(
            child: Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  
                  Image.asset(
                    'assets/images/logo.png',
                    width: 200,
                    height: 200,
                    fit: BoxFit.contain,
                  ),
                  
                  const SizedBox(height: 20),

                  // ΤΙΤΛΟΣ 
                  RichText(
                    textAlign: TextAlign.center,
                    text: const TextSpan(
                      style: TextStyle(
                        fontSize: 42, 
                        fontWeight: FontWeight.w900,
                        fontFamily: 'Arial',
                        height: 1.2,
                      ),
                      children: [
                        TextSpan(
                          text: "Meal",
                          style: TextStyle(color: Color(0xFF2D333B)), 
                        ),
                        TextSpan(
                          text: "Budget",
                          style: TextStyle(color: Color(0xFF2E8B57)), 
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 8),

                  const Text(
                    "Eat smart, save smart.",
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.black54,
                      fontWeight: FontWeight.w500,
                      letterSpacing: 1.1,
                    ),
                  ),

                  const SizedBox(height: 60),

                  // ΚΟΥΜΠΙ START
                  Container(
                    width: double.infinity,
                    height: 55,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF2E8B57).withOpacity(0.3),
                          blurRadius: 15,
                          offset: const Offset(0, 8), 
                        )
                      ],
                    ),
                    child: ElevatedButton(
                      onPressed: () => context.go('/params'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF2E8B57),
                        foregroundColor: Colors.white,
                        elevation: 0, 
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      child: const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            "Let's Start",
                            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                          ),
                          SizedBox(width: 10),
                          Icon(Icons.arrow_forward_rounded),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}