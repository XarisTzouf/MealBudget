import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'params_state.dart';
import '../../providers.dart';

class ParamsPage extends ConsumerStatefulWidget {
  const ParamsPage({super.key});

  @override
  ConsumerState<ParamsPage> createState() => _ParamsPageState();
}

class _ParamsPageState extends ConsumerState<ParamsPage> {
 
  late TextEditingController _budgetController;
  late TextEditingController _caloriesController;
  late TextEditingController _mealsController;

  @override
  void initState() {
    super.initState();
    final state = ref.read(paramsProvider);
    _budgetController = TextEditingController(text: state.budget.toString());
    _caloriesController = TextEditingController(text: state.calories.toString());
    _mealsController = TextEditingController(text: state.mealsPerDay.toString());
  }

  @override
  void dispose() {
    _budgetController.dispose();
    _caloriesController.dispose();
    _mealsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final paramsState = ref.watch(paramsProvider);
    final controller = ref.read(paramsProvider.notifier);

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text(
          "Plan Settings",
          style: TextStyle(color: Color(0xFF2D333B), fontWeight: FontWeight.bold),
        ),
        iconTheme: const IconThemeData(color: Color(0xFF2E8B57)),
      ),
      body: Stack(
        children: [
          // 1. ΦΟΝΤΟ 
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [Colors.white, Color(0xFFE8F5E9)],
              ),
            ),
          ),

          // 2. ΠΕΡΙΕΧΟΜΕΝΟ
          Center(
            child: SingleChildScrollView(
            
              padding: const EdgeInsets.fromLTRB(24, 110, 24, 20),
              child: Column(
                children: [
                  
                  Center(
                    child: Image.asset(
                      'assets/images/params_header.png', 
                      height: 120, 
                      fit: BoxFit.contain,
                    ),
                  ),
                  const SizedBox(height: 30), 

                  // Header Text 
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      "Set your goals 🎯",
                      style: TextStyle(
                        fontSize: 28, 
                        fontWeight: FontWeight.w800, 
                        color: Color(0xFF2D333B)
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      "Define your budget and nutrition targets.",
                      style: TextStyle(fontSize: 16, color: Colors.black54),
                    ),
                  ),
                  const SizedBox(height: 30),

                  // FORM CARD
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.grey.withOpacity(0.1), 
                          blurRadius: 20, 
                          offset: const Offset(0, 10)
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        _CustomTextField(
                          controller: _budgetController,
                          label: "Weekly Budget",
                          suffix: "€",
                          icon: Icons.savings_rounded,
                          onChanged: (val) => controller.updateBudget(double.tryParse(val) ?? 0),
                        ),
                        const SizedBox(height: 20),
                        _CustomTextField(
                          controller: _caloriesController,
                          label: "Daily Calories",
                          suffix: "kcal",
                          icon: Icons.bolt_rounded,
                          onChanged: (val) => controller.updateCalories(int.tryParse(val) ?? 0),
                        ),
                        const SizedBox(height: 20),
                        _CustomTextField(
                          controller: _mealsController,
                          label: "Meals per day",
                          suffix: "",
                          icon: Icons.restaurant_rounded,
                          onChanged: (val) => controller.updateMealsPerDay(int.tryParse(val) ?? 3),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 30),

                  // Error Message
                  if (paramsState.error != null)
                    Container(
                      padding: const EdgeInsets.all(12),
                      margin: const EdgeInsets.only(bottom: 20),
                      decoration: BoxDecoration(
                        color: Colors.red.shade50,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.red.shade200),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.error_outline, color: Colors.red),
                          const SizedBox(width: 12),
                          Expanded(child: Text(paramsState.error!, style: const TextStyle(color: Colors.red))),
                        ],
                      ),
                    ),

                  // GENERATE BUTTON
                  SizedBox(
                    width: double.infinity,
                    height: 60,
                    child: paramsState.isLoading
                        ? const Center(child: CircularProgressIndicator(color: Color(0xFF2E8B57)))
                        : ElevatedButton(
                            onPressed: () async {
                              FocusScope.of(context).unfocus();
                              final plan = await controller.submitOptimization();
                              
                              if (plan != null && context.mounted) {
                                ref.read(planResultProvider.notifier).state = plan;
                                context.go('/results');
                              }
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFF2E8B57),
                              foregroundColor: Colors.white,
                              elevation: 8,
                              shadowColor: const Color(0xFF2E8B57).withOpacity(0.4),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(16),
                              ),
                            ),
                            child: const Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.auto_awesome),
                                SizedBox(width: 12),
                                Text(
                                  "Generate Plan",
                                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                                ),
                              ],
                            ),
                          ),
                  ),

                  const SizedBox(height: 50), 
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// --- Helper Widget 
class _CustomTextField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final String suffix;
  final IconData icon;
  final Function(String) onChanged;

  const _CustomTextField({
    required this.controller,
    required this.label,
    required this.suffix,
    required this.icon,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: TextStyle(color: Colors.grey.shade600),
        suffixText: suffix,
        suffixStyle: const TextStyle(fontWeight: FontWeight.bold),
        prefixIcon: Icon(icon, color: const Color(0xFF2E8B57)),
        filled: true,
        fillColor: Colors.grey.shade50,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF2E8B57), width: 2),
        ),
      ),
      onChanged: onChanged,
    );
  }
}