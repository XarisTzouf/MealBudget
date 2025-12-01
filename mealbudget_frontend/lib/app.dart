import 'package:flutter/material.dart';
import 'core/app_router.dart';

class MealBudgetApp extends StatelessWidget {
  const MealBudgetApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: "MealBudget",
      routerConfig: router,
      theme: ThemeData(useMaterial3: true),
    );
  }
}
