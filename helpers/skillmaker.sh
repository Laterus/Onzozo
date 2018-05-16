read -p 'Skill Name: ' skillvar
read -p 'Description: ' descvar
read -p 'Modifier(int str def pow): ' modvar
read -p 'Scaling: ' nmunvar
read -p 'Cooldown: ' cldvar
read -p 'AOE(True or False): ' aoevar

echo
echo $skillvar:
echo "  "desc: "'$descvar'"
echo "  "mod: $modvar
echo "  "nmun: $nmunvar
echo "  "cld: $cldvar
echo "  "aoe: $aoevar
