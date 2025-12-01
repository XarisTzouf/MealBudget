

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/models.dart';
import '../../data/mealbudget_api.dart';
import '../../providers.dart';

// 1. State Class
class ParamsState {
  final double budget;
  final int calories;
  final int mealsPerDay;
  final bool isLoading;
  final String? error;

  ParamsState({
    this.budget = 50.0,
    this.calories = 2000,
    this.mealsPerDay = 3,
    this.isLoading = false,
    this.error,
  });

  ParamsState copyWith({
    double? budget,
    int? calories,
    int? mealsPerDay,
    bool? isLoading,
    String? error,
  }) {
    return ParamsState(
      budget: budget ?? this.budget,
      calories: calories ?? this.calories,
      mealsPerDay: mealsPerDay ?? this.mealsPerDay,
      isLoading: isLoading ?? this.isLoading,
      error: error, 
    );
  }
}

// 2. Controller Class
class ParamsController extends StateNotifier<ParamsState> {
  final MealBudgetApi _api;

  ParamsController(this._api) : super(ParamsState());

  void updateBudget(double value) => state = state.copyWith(budget: value);
  void updateCalories(int value) => state = state.copyWith(calories: value);
  void updateMealsPerDay(int value) => state = state.copyWith(mealsPerDay: value);

  // Η κύρια μέθοδος που καλείται όταν πατάς GENERATE PLAN
  Future<PlanResponse?> submitOptimization() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      // Ζητάμε τα πραγματικά προϊόντα από τη βάση δεδομένων
      final dbCandidates = await _api.getMeals();
      
      if (dbCandidates.isEmpty) {
        throw Exception("Database is empty! Run seed.py first.");
      }

      //  Φτιάχνουμε το Request
      final request = PlanRequest(
        title: "Weekly Plan (Optimized)",
        budget: state.budget,
        candidates: dbCandidates,
        kcalTarget: (state.calories * 7).toDouble(),);
        

      //  Κλήση στο Backend
      final response = await _api.optimizeBudget(request);
      
      state = state.copyWith(isLoading: false);
      return response;

    } catch (e) {
      print("Error: $e"); 
      state = state.copyWith(isLoading: false, error: e.toString());
      return null;
    }
  }
}

// 3. Provider Definition
final paramsProvider = StateNotifierProvider<ParamsController, ParamsState>((ref) {
  final api = ref.watch(mealBudgetApiProvider);
  return ParamsController(api);
});