
// lib/data/mealbudget_api.dart

import 'api_client.dart';
import '../core/models.dart';

class MealBudgetApi {
  final ApiClient client = ApiClient();

  Future<String> getHealth() async {
    final data = await client.get('/health');
    return data.toString();
  }

  // Λήψη των πραγματικών προϊόντων από τη βάση
  Future<List<PlanItemCandidate>> getMeals() async {
    final response = await client.get('/meals');
    final list = response as List;
    
    return list.map((json) {
      return PlanItemCandidate(
        mealId: json['id'],
        name: json['name'],
        category: json['category'] ?? 'main', 
        cost: (json['cost'] ?? 0).toDouble(),
        kcal: (json['kcal'] ?? 0).toDouble(),
        protein: (json['protein'] ?? 0).toDouble(),
        fat: (json['fat'] ?? 0).toDouble(),
        carbs: (json['carbs'] ?? 0).toDouble(),
      );
    }).toList();
  }

  Future<PlanRead> createPlan(PlanCreate body) async {
    final data = await client.post('/plans', data: body.toJson());
    return PlanRead.fromJson(data);
  }

  Future<PlanResponse> optimizeBudget(PlanRequest body) async {
    final data = await client.post('/budget/optimize', data: body.toJson());
    return PlanResponse.fromJson(data);
  }
}