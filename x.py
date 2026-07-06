# def removeExercise(self, name):
#     if self.doesExerciseExist(name):
#         for group in self.data['groups']:
#             self.removeExerciseFromGroup(name, group['name'])
#         exercises = [
#             exercise
#             for exercise in self.data['exercises']
#             if not (exercise == name)
#         ]
#         self.data['exercises'] = exercises
#         n = 0
#         while os.path.isfile(os.path.join(self.bin, name + str(n) + '.csv')):
#             n += 1
#         os.rename(os.path.join(self.trackers, name + '.csv'),
#                   os.path.join(self.bin, name + str(n) + '.csv'))
#     else:
#         logger.error('exercise does not exist')
#
# def addExerciseToGroup(self, exerciseName, groupName):
#     if exerciseName in self.data['exercises']:
#         for index in range(len(self.data['groups'])):
#             if self.data['groups'][index]['name'] == groupName:
#                 if exerciseName not in self.data['groups'][index]['exercises']:
#                     self.data['groups'][index]['exercises'].append(exerciseName)
#                     return
#     else:
#         logger.error('exercise does not exist')
#
# def removeExerciseFromGroup(self, exerciseName, groupName):
#     for index in range(len(self.data['groups'])):
#         if self.data['groups'][index]['name'] == groupName:
#             if exerciseName in self.data['exercises']:
#                 exercises = [exercise for exercise in self.data['groups'][index]['exercises'] if not (exercise == exerciseName)]
#                 self.data['groups'][index]['exercises'] = exercises
#                 return
#
#
# def removeGroup(self, name):
#     if self.doesGroupExist(name):
#         groups = [
#             group
#             for group in self.data['groups']
#             if not (group['name'] == name)
#         ]
#         self.data['groups'] = groups
#     else:
#         logger.error('group does not exist')
#
