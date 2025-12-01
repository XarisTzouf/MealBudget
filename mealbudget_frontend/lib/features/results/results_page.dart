import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:fl_chart/fl_chart.dart'; 

import '../../providers.dart';
import '../../core/models.dart';
import '../../widgets/kpi_card.dart';

class ResultsPage extends ConsumerWidget {
  const ResultsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final plan = ref.watch(planResultProvider);

    // Fallback αν δεν υπάρχουν δεδομένα
    if (plan == null) {
      return Scaffold(
        appBar: AppBar(title: const Text("Results")),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("No plan data found."),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => context.go('/params'), 
                child: const Text("Create New Plan"),
              ),
            ],
          ),
        ),
      );
    }

    // Κανονική Εμφάνιση
    return Scaffold(
      appBar: AppBar(title: Text(plan.title)),
      
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.go('/params'),
        label: const Text("Edit Params"),
        icon: const Icon(Icons.edit),
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.only(left: 16, right: 16, top: 16, bottom: 80),
        child: Column(
          children: [
            // KPIs
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Expanded(child: KpiCard(title: "TOTAL COST", value: "${plan.totalCost.toStringAsFixed(2)} €")),
                const SizedBox(width: 8),
                // ΔΙΟΡΘΩΣΗ 1: Αφαιρέθηκε το περιττό "${...}"
                Expanded(child: KpiCard(title: "TOTAL CALORIES", value: plan.totalKcal.toStringAsFixed(0))),
              ],
            ),
            const SizedBox(height: 24),

            // Γράφημα
            const Text("Macros Breakdown", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            MacroBarChart(plan: plan), 
            
            const SizedBox(height: 24),
            
            // Λίστα Φαγητών
            const Text("Shopping List / Meals", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const Divider(),
            
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: plan.rows.length,
              itemBuilder: (context, index) {
                final item = plan.rows[index];
                if (item.qty == 0) return const SizedBox.shrink();

                return Card(
                  margin: const EdgeInsets.symmetric(vertical: 4),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: Theme.of(context).colorScheme.primary,
                      foregroundColor: Colors.white,
                      child: Text("${item.qty}"),
                    ),
                    title: Text(item.name, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text("${item.kcal.toStringAsFixed(0)} kcal | ${item.cost.toStringAsFixed(2)} €/unit"),
                    trailing: Text(
                      "${(item.cost * item.qty).toStringAsFixed(2)} €",
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

// -----------------------------------------------------------------------------
// MacroBarChart Widget
// -----------------------------------------------------------------------------
class MacroBarChart extends StatelessWidget {
  final PlanResponse plan;

  const MacroBarChart({super.key, required this.plan});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          height: 200,
          child: BarChart(
            BarChartData(
              alignment: BarChartAlignment.spaceAround,
              maxY: _calculateMaxY(),
              barGroups: [
                // Protein (Red)
                BarChartGroupData(x: 0, barRods: [
                  BarChartRodData(toY: plan.totalProtein.toDouble(), color: Colors.redAccent, width: 20, borderRadius: BorderRadius.circular(4)),
                ]),
                // Fat (Green)
                BarChartGroupData(x: 1, barRods: [
                  BarChartRodData(toY: plan.totalFat.toDouble(), color: Colors.greenAccent, width: 20, borderRadius: BorderRadius.circular(4)),
                ]),
                // Carbs (Blue)
                BarChartGroupData(x: 2, barRods: [
                  BarChartRodData(toY: plan.totalCarbs.toDouble(), color: Colors.blueAccent, width: 20, borderRadius: BorderRadius.circular(4)),
                ]),
              ],
              titlesData: FlTitlesData(
                leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 40)),
                topTitles: const AxisTitles(),
                rightTitles: const AxisTitles(),
                bottomTitles: const AxisTitles(),
              ),
              gridData: const FlGridData(show: true, drawVerticalLine: false),
              borderData: FlBorderData(show: false),
            ),
          ),
        ),
        const SizedBox(height: 12),
        
        // ΔΙΟΡΘΩΣΗ 2: Προστέθηκαν τα const όπου χρειάζεται (γιατί αυτά δεν αλλάζουν ποτέ)
        const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _LegendItem(color: Colors.redAccent, text: "Protein (g)"),
            SizedBox(width: 16),
            _LegendItem(color: Colors.greenAccent, text: "Fat (g)"),
            SizedBox(width: 16),
            _LegendItem(color: Colors.blueAccent, text: "Carbs (g)"),
          ],
        ),
      ],
    );
  }

  double _calculateMaxY() {
    double maxVal = plan.totalProtein > plan.totalFat ? plan.totalProtein : plan.totalFat;
    if (plan.totalCarbs > maxVal) maxVal = plan.totalCarbs;
    return maxVal == 0 ? 100 : maxVal * 1.2;
  }
}

class _LegendItem extends StatelessWidget {
  final Color color;
  final String text;

  const _LegendItem({required this.color, required this.text});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(width: 12, height: 12, color: color),
        const SizedBox(width: 4),
        Text(text, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
      ],
    );
  }
}